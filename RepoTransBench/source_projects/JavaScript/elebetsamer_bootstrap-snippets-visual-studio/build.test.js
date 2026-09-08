const fs = require("fs");
const util = require("util");
const xml2js = require("xml2js");
const handlebars = require("handlebars");
const glob = require("glob");

jest.mock("fs");
jest.mock("glob");
jest.mock("xml2js");
jest.mock("handlebars");

describe("build.js main process", () => {
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

  test("copies LICENSE and generates snippet listing with correct parsing", (done) => {
    glob.mockImplementation((pattern, cb) => {
      cb(null, [
        "BootstrapSnippets/Snippets/HTML/Bootstrap/alert.snippet",
        "BootstrapSnippets/Snippets/HTML/Bootstrap/badge.snippet"
      ]);
    });

    let readFileCalls = 0;
    fs.readFile = jest.fn((file, opts, cb) => {
      if (typeof opts === "function") {
        cb = opts; // opts omitted
      }
      if (readFileCalls === 0) {
        cb(null, "<xml1/>");
      } else if (readFileCalls === 1) {
        cb(null, "<xml2/>");
      } else {
        cb(null, "template: {{snippets.length}}");
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
                Title: "Alert",
                Shortcut: "alert",
                Description: "Alert block"
              },
              Snippet: {
                Code: { $: { Language: "HTML" } },
                Declarations: {
                  Literal: {
                    ID: "type",
                    ToolTip: "Alert type",
                    Default: "alert-warning"
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
                Title: "Badge",
                Shortcut: "badge",
                Description: "Badge block"
              },
              Snippet: {
                Code: { $: { Language: "HTML" } },
                Declarations: {
                  Literal: [
                    { ID: "count", ToolTip: "Badge count", Default: "5" },
                    { ID: "label", ToolTip: "Badge label", Default: "New" }
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
        return ({ snippets }) => "output_md_" + snippets.length;
      }
    );

    jest.isolateModules(() => {
      require("./build.js");
    });

    setImmediate(() => {
      // LICENSE copy
      expect(fs.createReadStream).toHaveBeenCalledWith("LICENSE");
      expect(fs.createWriteStream).toHaveBeenCalledWith("BootstrapSnippets/LICENSE.txt");
      expect(glob).toHaveBeenCalled();
      expect(fs.readFile).toHaveBeenCalled();
      expect(handlebars.compile).toHaveBeenCalled();
      expect(fs.writeFileSync).toHaveBeenCalledWith("snippet-listing.md", "output_md_2");
      done();
    });
  });

  test("should handle edge case: no declarations present", (done) => {
    glob.mockImplementation((pattern, cb) => {
      cb(null, [
        "BootstrapSnippets/Snippets/HTML/Bootstrap/nodecl.snippet"
      ]);
    });

    fs.readFile = jest.fn((file, opts, cb) => {
      if (typeof opts === "function") {
        cb = opts;
      }
      if (file.includes('.snippet')) {
        cb(null, "<xml/>"); 
      } else {
        cb(null, "template dummy");
      }
    });

    xml2js.Parser.mockImplementation(() => ({
      parseString: (data, cb) => {
        cb(null, {
          CodeSnippet: {
            Header: {
              Title: "NoDecl",
              Shortcut: "nodecl",
              Description: "No declaration"
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
        return ({ snippets }) => "output_md_" + snippets.length;
      }
    );

    jest.isolateModules(() => {
      require("./build.js");
    });

    setImmediate(() => {
      expect(handlebars.compile).toHaveBeenCalled();
      expect(fs.writeFileSync).toHaveBeenCalled();
      done();
    });
  });

  test("should handle glob error gracefully", (done) => {
    glob.mockImplementation((pattern, cb) => {
      cb(new Error("Globbing failed"), null);
    });

    // track if processSnippets is called/writing is attempted
    fs.writeFileSync = jest.fn();
    handlebars.compile.mockImplementation(
      () => () => "output_md"
    );

    // The following will now avoid crashing even if glob errors
    jest.isolateModules(() => {
      require("./build.js");
    });

    setImmediate(() => {
      // Should not try to write a file if glob fails
      expect(fs.writeFileSync).not.toHaveBeenCalled();
      done();
    });
  });

  test("should handle file read error during snippet processing", (done) => {
    glob.mockImplementation((pattern, cb) => {
      cb(null, [
        "BootstrapSnippets/Snippets/HTML/Bootstrap/alert.snippet"
      ]);
    });

    let readFileCalls = 0;
    fs.readFile = jest.fn((file, opts, cb) => {
      if (typeof opts === "function") {
        cb = opts;
      }
      if (readFileCalls === 0) {
        cb(new Error("File read error"));
      } else {
        cb(null, "template: {{snippets.length}}");
      }
      readFileCalls++;
    });

    xml2js.Parser.mockImplementation(() => ({
      parseString: (data, cb) => {
        cb(null, {});
      }
    }));

    handlebars.compile.mockImplementation(
      () => () => "output_md"
    );

    jest.isolateModules(() => {
      require("./build.js");
    });

    setImmediate(() => {
      // If file read error, no .writeFileSync should be called
      expect(fs.writeFileSync).not.toHaveBeenCalled();
      done();
    });
  });

  test("should handle XML parse error", (done) => {
    glob.mockImplementation((pattern, cb) => {
      cb(null, [
        "BootstrapSnippets/Snippets/HTML/Bootstrap/alert.snippet"
      ]);
    });

    fs.readFile = jest.fn((file, opts, cb) => {
      if (typeof opts === "function") {
        cb = opts;
      }
      cb(null, "<xmlerr/>"); // Will parse error
    });

    xml2js.Parser.mockImplementation(() => ({
      parseString: (data, cb) => {
        cb(new Error("XML parsing error"));
      }
    }));

    handlebars.compile.mockImplementation(
      () => () => "output_md"
    );

    jest.isolateModules(() => {
      require("./build.js");
    });

    setImmediate(() => {
      expect(fs.writeFileSync).not.toHaveBeenCalled();
      done();
    });
  });
});