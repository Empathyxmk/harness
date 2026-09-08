package com.janetfilter.core.models;

import com.janetfilter.core.enums.RuleType;

public class FilterRule {
    private final RuleType type;
    private final String rule;
    public FilterRule(RuleType type, String rule) {
        this.type = type; this.rule = rule;
    }
    public RuleType getType() { return type; }
    public String getRule() { return rule; }
}