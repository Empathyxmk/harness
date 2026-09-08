#!/bin/bash
# Run only public tests. Since Maven doesn't have obvious public/private test scopes, we filter by *PublicTest in test class name.
mvn -Dtest=*PublicTest test