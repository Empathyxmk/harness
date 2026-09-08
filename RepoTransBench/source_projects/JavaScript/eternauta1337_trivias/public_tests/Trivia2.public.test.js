const assert = require('assert/strict');
const { ethers } = require('hardhat');

describe('Trivia2 (public tests)', function () {
  let Proxy, Instance, ImplementationV1, ImplementationV2;

  // ----------------------------------------------------------------
  // Implementation tests
  // ----------------------------------------------------------------

  function itBehavesLikeImplementationV1Public() {
    before('set value (public test)', async () => {
      // Public: use a distinct value
      const tx = await Instance.setValue('99');
      await tx.wait();
    });

    it('sets the value (public test)', async () => {
      assert.equal((await Instance.value()).toString(), '99');
    });
  }

  function itBehavesLikeImplementationV2Public() {
    before('set addr (public test)', async () => {
      // Public: use a different address (last byte 0x99)
      const tx = await Instance.setAddr('0x0000000000000000000000000000000000000099');
      await tx.wait();
    });

    it('sets the addr (public test)', async () => {
      assert.equal((await Instance.addr()).toString(), '0x0000000000000000000000000000000000000099');
    });
  }

  // ----------------------------------------------------------------
  // Transparent proxies
  // ----------------------------------------------------------------

  describe('when using transparent proxies (public test)', () => {
    before('deploy the proxy with the first implementation', async () => {
      let factory;

      // Deploy the first implementation
      factory = await ethers.getContractFactory('ImplementationV1_t2');
      ImplementationV1 = await factory.deploy();

      // Deploy the proxy and set its first implementation
      factory = await ethers.getContractFactory('TransparentProxy_t2');
      Proxy = await factory.deploy(ImplementationV1.address);

      // Disguise the proxy as the implementation
      Instance = await ethers.getContractAt('ImplementationV1_t2', Proxy.address);
    });

    it('shows that the implementation is set (public test)', async () => {
      // We ask the proxy about its implementation
      assert.equal(await Proxy.getImplementation(), ImplementationV1.address);
    });

    itBehavesLikeImplementationV1Public();

    describe('when upgrading to V2 (public test)', () => {
      before('upgrade', async () => {
        // Deploy the second implementation
        const factory = await ethers.getContractFactory('ImplementationV2_t2');
        ImplementationV2 = await factory.deploy();

        // Upgrade the proxy
        const tx = await Proxy.upgradeTo(ImplementationV2.address);
        await tx.wait();

        // Disguise the proxy as the new implementation
        Instance = await ethers.getContractAt('ImplementationV2_t2', Proxy.address);
      });

      it('shows that the implementation is set (public test)', async () => {
        assert.equal(await Proxy.getImplementation(), ImplementationV2.address);
      });

      itBehavesLikeImplementationV1Public();
      itBehavesLikeImplementationV2Public();
    });
  });

  // ----------------------------------------------------------------
  // Universal proxies
  // ----------------------------------------------------------------

  describe('when using universal proxies (public test)', () => {
    before('deploy the proxy with the first implementation', async () => {
      let factory;

      // Deploy the first implementation
      factory = await ethers.getContractFactory('UniversalImplementationV1_t2');
      ImplementationV1 = await factory.deploy();

      // Deploy the proxy and set its first implementation
      factory = await ethers.getContractFactory('UniversalProxy_t2');
      Proxy = await factory.deploy(ImplementationV1.address);

      // Disguise the proxy as the implementation
      Instance = await ethers.getContractAt('UniversalImplementationV1_t2', Proxy.address);
    });

    it('shows that the implementation is set (public test)', async () => {
      // We ask the instance about its implementation
      assert.equal(await Instance.getImplementation(), ImplementationV1.address);
    });

    itBehavesLikeImplementationV1Public();

    describe('when upgrading to V2 (public test)', () => {
      before('upgrade', async () => {
        // Deploy the second implementation
        const factory = await ethers.getContractFactory('UniversalImplementationV2_t2');
        ImplementationV2 = await factory.deploy();

        // Upgrade the proxy via the implementation
        const tx = await Instance.upgradeTo(ImplementationV2.address);
        await tx.wait();

        // Disguise the proxy as the new implementation
        Instance = await ethers.getContractAt('UniversalImplementationV2_t2', Proxy.address);
      });

      it('shows that the implementation is set (public test)', async () => {
        assert.equal(await Instance.getImplementation(), ImplementationV2.address);
      });

      itBehavesLikeImplementationV1Public();
      itBehavesLikeImplementationV2Public();
    });
  });
});