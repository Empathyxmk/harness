# ⚠️ Tests Cannot Be Run: Build Configuration Incompatible

## Summary

- **Build failure due to:**
  - `Unsupported class file major version 61` (class files built with Java 17+)
  - Gradle version or Groovy dependencies incompatible with Java 17 bytecode

- **Status:**
  - Test runner scripts exist
  - Public tests are present with different test data
  - **But neither private nor public tests can be verified due to build tool incompatibility**

---

## What Needs Fixing

1. **Determine the required JDK and Gradle versions:**
   - Either downgrade code to Java 8/11 *or* upgrade Gradle (and Android Gradle plugin) to support Java 17.
2. **Regenerate any precompiled JARs/classes with consistent JDK/tooling.**
3. **Only then can tests be reliably executed.**

---

Until this is fixed by the repository maintainer, both test passes and public test verification are not possible.