// index.test.js
const fs = require("fs");

describe("kristerkari-react-native-svg-transformer", () => {
  beforeEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
    jest.restoreAllMocks?.();
  });

  describe("getExpoTransformer", () => {
    it("should return the expo transformer if module exists", () => {
      jest.doMock(
        "@expo/metro-config/babel-transformer",
        () => ({
          transform: jest.fn(),
        }),
        { virtual: true }
      );
      const { getExpoTransformer } = require("./index");
      const transformer = getExpoTransformer();
      expect(transformer).toBeDefined();
      expect(typeof transformer.transform).toBe("function");
      jest.dontMock("@expo/metro-config/babel-transformer");
    });

    it("should return null if @expo/metro-config/babel-transformer not found", () => {
      jest.resetModules();
      try {
        jest.requireActual("@expo/metro-config/babel-transformer");
        // should throw
        expect(false).toBe(true);
      } catch (e) {
        // simulate absence by deleting from require cache and not mocking
        jest.isolateModules(() => {
          const { getExpoTransformer } = require("./index");
          const transformer = getExpoTransformer();
          expect(transformer).toBeNull();
        });
      }
    });
  });

  describe("main exported transformer", () => {
    it("should return {code: undefined} if src is not a string", async () => {
      const mod = require("./index");
      const result = await mod.transform({ src: null, filename: "not-an-svg.png", options: {} });
      expect(result).toEqual({ code: undefined }); // should be a normal return, not a Promise
    });

    it("should transform svg with expo transformer present", async () => {
      jest.doMock(
        "@expo/metro-config/babel-transformer",
        () => ({
          transform: jest.fn().mockReturnValue({ code: "expo" }),
        }),
        { virtual: true }
      );
      jest.doMock("@svgr/core", () => ({ transform: jest.fn().mockResolvedValue("expoSvg") }), { virtual: true });
      const mod = require("./index");
      const result = await mod.transform({
        src: "<svg></svg>",
        filename: "icon.svg",
        options: { dev: true },
      });
      expect(result).toHaveProperty("code", "expo");
      jest.dontMock("@expo/metro-config/babel-transformer");
      jest.dontMock("@svgr/core");
    });

    it("should handle custom config (svgrConfigFile exists)", async () => {
      jest.doMock(
        "@expo/metro-config/babel-transformer",
        () => ({
          transform: jest.fn().mockReturnValue({ code: "withcfg" }),
        }),
        { virtual: true }
      );
      jest.doMock("@svgr/core", () => ({ transform: jest.fn().mockResolvedValue("svgcontent") }), { virtual: true });
      jest.doMock("path-dirname", () => (file) => "", { virtual: true });
      jest.spyOn(fs, "existsSync").mockImplementation((file) =>
        file === ".svgrrc"
      );
      jest.spyOn(fs, "readFileSync").mockImplementation((file) =>
        file === ".svgrrc" ? JSON.stringify({ foo: "bar" }) : ""
      );
      const mod = require("./index");
      const result = await mod.transform({
        src: "<svg></svg>",
        filename: "icon.svg",
        options: { dev: true, svgrConfigFile: ".svgrrc" },
      });
      expect(result).toEqual({ code: "withcfg" });
      fs.existsSync.mockRestore();
      fs.readFileSync.mockRestore();
      jest.dontMock("@expo/metro-config/babel-transformer");
      jest.dontMock("@svgr/core");
      jest.dontMock("path-dirname");
    });

    it("should fall back if custom config not found and transform with default config", async () => {
      jest.doMock(
        "@expo/metro-config/babel-transformer",
        () => ({
          transform: jest.fn().mockReturnValue({ code: "defaultcfg" }),
        }),
        { virtual: true }
      );
      jest.doMock("@svgr/core", () => ({ transform: jest.fn().mockResolvedValue("svg2") }), { virtual: true });
      jest.doMock("path-dirname", () => (file) => "", { virtual: true });
      jest.spyOn(fs, "existsSync").mockReturnValue(false);
      const mod = require("./index");
      const result = await mod.transform({
        src: "<svg></svg>",
        filename: "icon.svg",
        options: { dev: true, svgrConfigFile: ".notfound" },
      });
      expect(result).toEqual({ code: "defaultcfg" });
      fs.existsSync.mockRestore();
      jest.dontMock("@expo/metro-config/babel-transformer");
      jest.dontMock("@svgr/core");
      jest.dontMock("path-dirname");
    });

    it("should transform using fallback metro transformer if expo transformer missing", async () => {
      jest.resetModules();
      jest.doMock("./react-native", () => ({
        transform: jest.fn().mockReturnValue({ code: "defaultcfg" }),
      }), { virtual: true });
      jest.doMock("@svgr/core", () => ({ transform: jest.fn().mockResolvedValue("running") }), { virtual: true });
      // Simulate expo not found by not mocking it at all
      const mod = require("./index");
      const result = await mod.transform({
        src: "<svg></svg>",
        filename: "icon.svg",
        options: { dev: false }
      });
      expect(result).toEqual({ code: "defaultcfg" });
      jest.dontMock("./react-native");
      jest.dontMock("@svgr/core");
    });

    it("should handle thrown errors gracefully in config reading", async () => {
      jest.doMock("@expo/metro-config/babel-transformer", () => ({
        transform: jest.fn().mockReturnValue({ code: "expo" }),
      }), { virtual: true });
      jest.doMock("@svgr/core", () => ({ transform: jest.fn().mockResolvedValue("svg") }), { virtual: true });
      jest.doMock("path-dirname", () => (file) => "", { virtual: true });
      jest.spyOn(fs, "existsSync").mockImplementation(() => true);
      jest.spyOn(fs, "readFileSync").mockImplementation(() => { throw new Error("fail"); });
      const mod = require("./index");
      // Should not throw, just not use the config file
      const result = await mod.transform({
        src: "<svg></svg>",
        filename: "icon.svg",
        options: { dev: true, svgrConfigFile: ".svgrrc" }
      });
      expect(result).toEqual({ code: "expo" });
      fs.existsSync.mockRestore();
      fs.readFileSync.mockRestore();
      jest.dontMock("@expo/metro-config/babel-transformer");
      jest.dontMock("@svgr/core");
      jest.dontMock("path-dirname");
    });
  });
});