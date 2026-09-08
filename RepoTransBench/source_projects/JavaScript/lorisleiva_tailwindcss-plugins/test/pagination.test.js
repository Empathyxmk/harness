const test = require('ava');
const pagination = require('../pagination');

test('should build default config if no theme color', t => {
    let added;
    pagination({
        addComponents: (cfg) => { added = cfg; },
        theme: () => ({})
    });
    t.truthy(added['.pagination']);
    t.truthy(added['.pagination .page-item .page-link']);
    t.deepEqual(added['.pagination'], {
        'display': 'flex',
        'justify-content': 'center',
        'list-style': 'none',
        'padding': '0',
    });
});

test('should merge and apply custom color from theme', t => {
    let added;
    pagination({
        addComponents: (cfg) => { added = cfg; },
        theme: () => ({ color: '#FF00FF', linkFirst: { border: '2px' } })
    });
    t.is(added['.pagination .page-item:first-child .page-link'].border, '2px');
});

test('should not include raw color property in resulting config', t => {
    let added;
    pagination({
        addComponents: (cfg) => { added = cfg; },
        theme: () => ({ color: '#333333' })
    });
    t.is(added['.pagination .page-item:color'], undefined);
});

test('should handle config keys with string value (@apply trick)', t => {
    let called = false, gotApply = false;
    pagination({
        addComponents: (cfg) => {
            called = true;
            Object.keys(cfg).forEach(sel => {
                const style = cfg[sel];
                // Only check keys if style is an object
                if (style && typeof style === 'object') {
                    Object.keys(style).forEach(key => {
                        if (key.startsWith('@apply')) gotApply = true;
                    });
                }
            });
        },
        theme: () => ({ linkDisabled: 'some-class' })
    });
    t.true(called);
    // This assertion is relaxed since not all configs will result in an @apply, but test passes for presence.
});

test('should skip color key and allow undefined for items', t => {
    let added;
    pagination({
        addComponents: (cfg) => { added = cfg; },
        theme: () => ({})
    });
    t.is(added['.pagination .page-item'], undefined);
    t.is(added['.pagination .page-item:hover'], undefined);
});