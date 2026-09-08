const expect = require('chai').expect;

describe('delivery/severalStrategies (public)', function () {
    it('should allow multiple different strategies', function () {
        let strategies = [];

        function addDelivery(strat) {
            if (!strat || typeof strat.sendToken !== 'function')
                throw new Error('Bad strategy');
            strategies.push(strat);
        }

        addDelivery({ sendToken: () => {} });
        addDelivery({ sendToken: () => {} });

        expect(strategies.length).to.equal(2);
    });
});