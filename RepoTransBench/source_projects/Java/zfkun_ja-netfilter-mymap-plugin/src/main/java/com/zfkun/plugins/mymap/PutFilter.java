package com.zfkun.plugins.mymap;

import com.janetfilter.core.commons.DebugInfo;
import com.janetfilter.core.models.FilterRule;

import java.util.List;

public class PutFilter {
    private List<FilterRule> rules;

    public PutFilter(List<FilterRule> rules) {
        this.rules = rules;
    }

    public boolean shouldAllow(String key) {
        if (rules == null || rules.isEmpty() || key == null) {
            DebugInfo.output("Allow: no rules or key is null");
            return true;
        }
        for (FilterRule rule : rules) {
            if (rule == null || rule.getType() == null || rule.getRule() == null) continue;
            switch (rule.getType()) {
                case EQUAL:
                    if (key.equals(rule.getRule())) {
                        DebugInfo.output("Blocked equal: " + key);
                        return false;
                    }
                    break;
                case CONTAINS:
                    if (key.contains(rule.getRule())) {
                        DebugInfo.output("Blocked contains: " + key);
                        return false;
                    }
                    break;
                default:
                    // pass
            }
        }
        DebugInfo.output("Allow: passed all rules");
        return true;
    }
}