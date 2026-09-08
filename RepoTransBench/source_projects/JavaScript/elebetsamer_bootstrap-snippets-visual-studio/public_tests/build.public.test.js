const fs = require("fs");
const util = require("util");
const xml2js = require("xml2js");
const handlebars = require("handlebars");
const glob = require("glob");

jest.mock("fs");
jest.mock("glob");
jest.mock("xml2js");
jest.mock("handlebars");

describe("build.js main process (public tests)", () => {
  let originalCreateReadStream, originalCreateWriteStream, originalReadFile, originalWriteFileSync;

  beforeAll(() => {
    // Prepare fs mocks for createReadStream/WriteStream
    originalCreateReadStream = fs.createReadStream;
    originalCreateWriteStream = fs.createWriteStream;
    originalReadFile = fs.readFile;
    originalWriteFileSync = fs.writeFileSync;

    // Mocks for LICENSE copy
    fs.createReadStream = jest.fn(() => ({
      pipe: jest.fn()
    }));

    fs.createWriteStream = jest.fn();

    // Mock util.isArray
    util.isArray = Array.isArray;

    fs.writeFileSync = jest.fn();
  });

  afterAll(() => {
    fs.createReadStream = originalCreateReadStream;
    fs.createWriteStream = originalCreateWriteStream;
    fs.readFile = originalReadFile;
    fs.writeFileSync = originalWriteFileSync;
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test("copies LICENSE and generates snippet listing with alternate parsing", (done) => {
    glob.mockImplementation((pattern, cb) => {
      cb(null, [
        "BootstrapSnippets/Snippets/HTML/Bootstrap/carousel.snippet",
        "BootstrapSnippets/Snippets/HTML/Bootstrap/input-group.snippet"
      ]);
    });

    let readFileCalls = 0;
    fs.readFile = jest.fn((file, opts, cb) => {
      if (typeof opts === "function") {
        cb = opts; // opts omitted
      }
      if (readFileCalls === 0) {
        cb(null, "<xmlA/>");
      } else if (readFileCalls === 1) {
        cb(null, "<xmlB/>");
      } else {
        cb(null, "template: {{snippetsCount}}");
      }
      readFileCalls++;
    });

    // Mock xml2js.Parser and parser.parseString
    const parseStringMock = jest.fn();
    xml2js.Parser.mockImplementation(() => ({
      parseString: parseStringMock
    }));

    let parseCall = 0;
    parseStringMock.mockImplementation((data, cb) => {
      parseCall++;
      if (parseCall === 1) {
        cb(
          null,
          {
            CodeSnippet: {
              Header: {
                Title: "Carousel",
                Shortcut: "carousel",
                Description: "Carousel component"
              },
              Snippet: {
                Code: { $: { Language: "HTML" } },
                Declarations: {
                  Literal: {
                    ID: "slides",
                    ToolTip: "Number of slides",
                    Default: "3"
                  }
                }
              }
            }
          }
        );
      } else if (parseCall === 2) {
        cb(
          null,
          {
            CodeSnippet: {
              Header: {
                Title: "Input Group",
                Shortcut: "input-group",
                Description: "Input group field"
              },
              Snippet: {
                Code: { $: { Language: "HTML" } },
                Declarations: {
                  Literal: [
                    { ID: "addon", ToolTip: "Addon String", Default: "+" },
                    { ID: "size", ToolTip: "Input size", Default: "lg" }
                  ]
                }
              }
            }
          }
        );
      } else {
        cb(null, {});
      }
    });

    handlebars.compile.mockImplementation(
      (templateStr) => {
        return ({ snippets }) => "public_output_md_" + snippets.length;
      }
    );

    jest.isolateModules(() => {
      require("../build.js");
    });

    setImmediate(() => {
      // LICENSE copy
      expect(fs.createReadStream).toHaveBeenCalledWith("LICENSE");
      expect(fs.createWriteStream).toHaveBeenCalledWith("BootstrapSnippets/LICENSE.txt");
      expect(glob).toHaveBeenCalled();
      expect(fs.readFile).toHaveBeenCalled();
      expect(handlebars.compile).toHaveBeenCalled();
      expect(fs.writeFileSync).toHaveBeenCalledWith("snippet-listing.md", "public_output_md_2");
      done();
    });
  });

  test("should handle edge: no declarations present, public", (done) => {
    glob.mockImplementation((pattern, cb) => {
      cb(null, [
        "BootstrapSnippets/Snippets/HTML/Bootstrap/justcode.snippet"
      ]);
    });

    fs.readFile = jest.fn((file, opts, cb) => {
      if (typeof opts === "function") {
        cb = opts;
      }
      if (file.includes('.snippet')) {
        cb(null, "<xmlOnlyCode/>"); 
      } else {
        cb(null, "template-file");
      }
    });

    xml2js.Parser.mockImplementation(() => ({
      parseString: (data, cb) => {
        cb(null, {
          CodeSnippet: {
            Header: {
              Title: "JustCode",
              Shortcut: "justcode",
              Description: "No declarations here"
            },
            Snippet: {
              Code: { $: { Language: "HTML" } }
            }
          }
        });
      }
    }));

    handlebars.compile.mockImplementation(
      (templateStr) => {
        return ({ snippets }) => "public_output_md_" + snippets.length;
      }
    );

    jest.isolateModules(() => {
      require("../build.js");
    });

    setImmediate(() => {
      expect(handlebars.compile).toHaveBeenCalled();
      expect(fs.writeFileSync).toHaveBeenCalled();
      done();
    });
  });

  test("should handle glob error gracefully (public)", (done) => {
    glob.mockImplementation((pattern, cb) => {
      cb(new Error("Pattern not matching"), null);
    });

    fs.writeFileSync = jest.fn();
    handlebars.compile.mockImplementation(
      () => () => "publicOutput"
    );

    jest.isolateModules(() => {
      require("../build.js");
    });

    setImmediate(() => {
      expect(fs.writeFileSync).not.toHaveBeenCalled();
      done();
    });
  });

  test("should handle file read error during snippet processing (public)", (done) => {
    glob.mockImplementation((pattern, cb) => {
      cb(null, [
        "BootstrapSnippets/Snippets/HTML/Bootstrap/carousel.snippet"
      ]);
    });

    let readFileCalls = 0;
    fs.readFile = jest.fn((file, opts, cb) => {
      if (typeof opts === "function") {
        cb = opts;
      }
      if (readFileCalls === 0) {
        cb(new Error("Test file read fail"));
      } else {
        cb(null, "template: {{snippetsList}}");
      }
      readFileCalls++;
    });

    xml2js.Parser.mockImplementation(() => ({
      parseString: (data, cb) => {
        cb(null, {});
      }
    }));

    handlebars.compile.mockImplementation(
      () => () => "another_md"
    );

    jest.isolateModules(() => {
      require("../build.js");
    });

    setImmediate(() => {
      // Still shouldn't write anything
      expect(fs.writeFileSync).not.toHaveBeenCalled();
      done();
    });
  });
});