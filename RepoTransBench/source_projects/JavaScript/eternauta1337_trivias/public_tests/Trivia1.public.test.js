const assert = require('assert/strict');
const { ethers } = require('hardhat');

describe('Trivia1 (public tests)', function () {
  let ContractA, ContractB;

  let user;

  let errors, records;

  before('identify signers', async () => {
    ([user] = await ethers.getSigners());
  });

  before('deploy the contracts', async () => {
    let factory;

    factory = await ethers.getContractFactory('ContractA_t1');
    ContractA = await factory.deploy();

    factory = await ethers.getContractFactory('ContractB_t1');
    ContractB = await factory.deploy();
  });

  async function multipleCallsWithMethod(method, times) {
    async function call() {
      let receipt;

      try {
        // On public test, call with ContractA as the first argument as in original
        const tx = await ContractA[method](ContractB.address);
        receipt = await tx.wait();
      } catch (error) {
        errors.push(error.toString());
      }

      if (receipt && receipt.events.length > 0) {
        const event = receipt.events[0];
        records.push(event.args[0]);
      }
    }

    errors = [];
    records = [];

    for (let i = 0; i < times; i++) {
      await call();
    }
  }

  describe('when using the first method', () => {
    before('call method1 three times', async () => {
      await multipleCallsWithMethod('method1', 3)
    });

    it('will have reverted twice with the expected error', async () => {
      // Change: called three times instead of two, expecting two errors
      assert.equal(errors.length, 2);
      // Check at least the error string contains the revert reason
      assert(errors[0].toString().includes('reverted with reason string \'Nope!\''));
      assert(errors[1].toString().includes('reverted with reason string \'Nope!\''));
    });

    it('will have recorded contract A as the sender', async () => {
      assert.equal(records.length, 1);
      assert.equal(records[0], ContractA.address);
    });
  });

  describe('when using the second method', () => {
    before('call method2 four times', async () => {
      await multipleCallsWithMethod('method2', 4)
    });

    it('will not have reverted', async () => {
      assert.equal(errors.length, 0);
    });

    it('will have recorded contract A as the sender', async () => {
      assert.equal(records.length, 1);
      assert.equal(records[0], ContractA.address);
    });
  });

  describe('when using the third method', () => {
    before('call method3 once', async () => {
      await multipleCallsWithMethod('method3', 1)
    });

    it('will not have reverted', async () => {
      assert.equal(errors.length, 0);
    });

    it('will have recorded the user as the sender', async () => {
      assert.equal(records.length, 1);
      assert.equal(records[0], user.address);
    });
  });
});