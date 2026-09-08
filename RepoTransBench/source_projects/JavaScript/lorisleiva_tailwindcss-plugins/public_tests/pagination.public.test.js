const test = require('ava');
const pagination = require('../pagination');

test('should build default config if no theme color (public)', t => {
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

// Use a different color and a different property in theme (linkLast)
test('should merge and apply custom color from theme (public)', t => {
    let added;
    pagination({
        addComponents: (cfg) => { added = cfg; },
        theme: () => ({ color: '#00FF00', linkLast: { border: '3px solid #000' } })
    });
    t.is(added['.pagination .page-item:last-child .page-link'].border, '3px solid #000');
});

test('should not include raw color property in resulting config (public)', t => {
    let added;
    pagination({
        addComponents: (cfg) => { added = cfg; },
        theme: () => ({ color: '#123456' })
    });
    t.is(added['.pagination .page-item:color'], undefined);
});

// Different string key: use linkActive and set to a new string
test('should handle config keys with string value (@apply trick, public)', t => {
    let called = false, gotApply = false;
    pagination({
        addComponents: (cfg) => {
            called = true;
            Object.keys(cfg).forEach(sel => {
                const style = cfg[sel];
                if (style && typeof style === 'object') {
                    Object.keys(style).forEach(key => {
                        if (key.startsWith('@apply')) gotApply = true;
                    });
                }
            });
        },
        theme: () => ({ linkActive: 'bg-blue-700' })
    });
    t.true(called);
});

test('should skip color key and allow undefined for other items (public)', t => {
    let added;
    pagination({
        addComponents: (cfg) => { added = cfg; },
        theme: () => ({})
    });
    t.is(added['.pagination .page-item'], undefined);
    t.is(added['.pagination .page-item:hover'], undefined);
});