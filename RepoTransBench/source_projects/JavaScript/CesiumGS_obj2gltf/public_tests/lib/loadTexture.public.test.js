"use strict";
const loadTexture = require("../../lib/loadTexture");

const altPngTexturePath = "specs/data/box-texture-options/bump.png";
const altJpgTexturePath = "specs/data/box-complex-material-alpha/emission.jpg";
const altJpegTexturePath = "specs/data/box-complex-material-alpha/specular.jpeg";
const altGifTexturePath = "specs/data/box-texture-options/ambient.gif";
const altGrayscaleTexturePath = "specs/data/box-complex-material-alpha/alpha.png";
const altTransparentTexturePath = "specs/data/box-complex-material-alpha/diffuse.png";

describe("loadTexture (public)", () => {
  it("loads alternative png texture", async () => {
    const texture = await loadTexture(altPngTexturePath);
    expect(texture.transparent).toBe(false);
    expect(texture.source).toBeDefined();
    expect(texture.name).toBe("bump");
    expect(texture.extension).toBe(".png");
    expect(texture.path).toBe(altPngTexturePath);
    expect(texture.pixels).toBeUndefined();
    expect(texture.width).toBeUndefined();
    expect(texture.height).toBeUndefined();
  });

  it("loads alternative jpg texture", async () => {
    const texture = await loadTexture(altJpgTexturePath);
    expect(texture.transparent).toBe(false);
    expect(texture.source).toBeDefined();
    expect(texture.name).toBe("emission");
    expect(texture.extension).toBe(".jpg");
    expect(texture.path).toBe(altJpgTexturePath);
    expect(texture.pixels).toBeUndefined();
    expect(texture.width).toBeUndefined();
    expect(texture.height).toBeUndefined();
  });

  it("loads alternative jpeg texture", async () => {
    const texture = await loadTexture(altJpegTexturePath);
    expect(texture.transparent).toBe(false);
    expect(texture.source).toBeDefined();
    expect(texture.name).toBe("specular");
    expect(texture.extension).toBe(".jpeg");
    expect(texture.path).toBe(altJpegTexturePath);
    expect(texture.pixels).toBeUndefined();
    expect(texture.width).toBeUndefined();
    expect(texture.height).toBeUndefined();
  });

  it("loads alternative gif texture", async () => {
    const texture = await loadTexture(altGifTexturePath);
    expect(texture.transparent).toBe(false);
    expect(texture.source).toBeDefined();
    expect(texture.name).toBe("ambient");
    expect(texture.extension).toBe(".gif");
    expect(texture.path).toBe(altGifTexturePath);
    expect(texture.pixels).toBeUndefined();
    expect(texture.width).toBeUndefined();
    expect(texture.height).toBeUndefined();
  });

  it("loads alternative grayscale texture", async () => {
    const texture = await loadTexture(altGrayscaleTexturePath);
    expect(texture.transparent).toBe(true);
    expect(texture.source).toBeDefined();
    expect(texture.name).toBe("alpha");
    expect(texture.extension).toBe(".png");
    expect(texture.path).toBe(altGrayscaleTexturePath);
    expect(texture.pixels).toBeUndefined();
    expect(texture.width).toBeUndefined();
    expect(texture.height).toBeUndefined();
  });

  it("loads alternative transparent texture", async () => {
    const texture = await loadTexture(altTransparentTexturePath);
    expect(texture.transparent).toBe(true);
    expect(texture.source).toBeDefined();
    expect(texture.name).toBe("diffuse");
    expect(texture.extension).toBe(".png");
    expect(texture.path).toBe(altTransparentTexturePath);
    expect(texture.pixels).toBeUndefined();
    expect(texture.width).toBeUndefined();
    expect(texture.height).toBeUndefined();
  });
});