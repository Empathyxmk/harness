const _ = require('lodash');
const Vue = require("vue");
const VueModel = require('../src/VueModel');

describe("VueModel (public)", () => {

    // This is need because Vue.use caches installed plugins
    var fakeVueUse = (plugin, ...args) => {
        plugin.install.apply(plugin, [Vue].concat(args));
    };

    describe("Vue.models.register() public spec", () => {
        beforeEach(() => {
            VueModel.registry = {};
            spyOn(VueModel, 'register').and.callThrough && spyOn(VueModel, 'register').and.callThrough();
        });

        it("registers model(s) with another dataset", () => {
            expect(VueModel.register).not.toHaveBeenCalled();

            fakeVueUse(VueModel);

            const baseRoute = '/mywidgets'

            Vue.models.register('foo', {
                http: {
                    baseRoute
                }
            });

            expect(VueModel.register).toHaveBeenCalled();
            expect(VueModel.registry.foo).toBeTruthy();
            expect(_.get(VueModel.registry.foo, 'http.baseRoute')).toBe(baseRoute);
        });

        it("registers model(s) with Vue.use, other input", () => {
            expect(VueModel.register).not.toHaveBeenCalled();
            const baseRoute = '/barwidgets'

            fakeVueUse(VueModel, {
                qux: {
                    http: {
                        baseRoute
                    }
                }
            });

            expect(VueModel.register).toHaveBeenCalled();
            expect(VueModel.registry.qux).toBeTruthy();
            expect(_.get(VueModel.registry.qux, 'http.baseRoute')).toBe(baseRoute);
        });
    });
});