package com.zfkun.plugins.mymap;

import com.janetfilter.core.Environment;
import com.janetfilter.core.plugin.PluginConfig;
import com.janetfilter.core.plugin.PluginEntry;
import com.janetfilter.core.plugin.MyTransformer;

import java.util.Collections;
import java.util.List;

public class MyPluginEntry implements PluginEntry {
    private List<MyTransformer> transformers;

    @Override
    public void init(Object environment, PluginConfig config) {
        // Typically config parsing; for stub assume fixed plugins
        this.transformers = Collections.singletonList(new MapTransformer(null));
    }

    @Override
    public String getName() {
        return "MyMapPlugin";
    }

    @Override
    public String getAuthor() {
        return "zfkun";
    }

    @Override
    public String getVersion() {
        return "1.0.0";
    }

    @Override
    public String getDescription() {
        return "A plugin to filter map puts.";
    }

    @Override
    public List<? extends MyTransformer> getTransformers() {
        return transformers;
    }
}