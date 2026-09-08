package com.janetfilter.core.plugin;

import java.util.List;

public interface PluginEntry {
    void init(Object environment, PluginConfig config);
    String getName();
    String getAuthor();
    String getVersion();
    String getDescription();
    List<? extends MyTransformer> getTransformers();
}