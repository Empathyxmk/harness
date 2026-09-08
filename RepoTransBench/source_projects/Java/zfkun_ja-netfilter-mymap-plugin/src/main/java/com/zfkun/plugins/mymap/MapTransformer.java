package com.zfkun.plugins.mymap;

import com.janetfilter.core.models.FilterRule;
import com.janetfilter.core.plugin.MyTransformer;

import java.util.ArrayList;
import java.util.List;

public class MapTransformer implements MyTransformer {
    private List<FilterRule> rules = new ArrayList<>();

    public MapTransformer(List<FilterRule> rules) {
        if (rules != null) {
            this.rules.addAll(rules);
        }
    }

    public boolean containsRule(String input) {
        if (input == null) return false;
        for (FilterRule rule : rules) {
            if (rule == null || rule.getRule() == null || rule.getType() == null) continue;
            switch (rule.getType()) {
                case EQUAL:
                    if (input.equals(rule.getRule())) return true;
                    break;
                case CONTAINS:
                    if (input.contains(rule.getRule())) return true;
                    break;
                default:
                    // ignore
            }
        }
        return false;
    }

    public List<FilterRule> getRules() {
        return rules;
    }
}