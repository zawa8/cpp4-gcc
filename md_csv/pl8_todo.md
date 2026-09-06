# pl8 Type System - TODO

## Completed
- RID_PL8 keyword added
- pl8_type_node defined
- TI_PL8_TYPE enum added
- record_builtin_type updated

## Pending
1. pl8 struct define (digits array, start_pl, sign)
2. pl8 literal parsing (-5VFFFF.5V5V5V format)
3. Arithmetic operations (add, sub, mul, div)
4. Comparison operators
5. Type checking rules
6. Code generation
7. Runtime library (cplong port to C++)

## Next Steps
1. Define pl8 tree code (separate from REAL_TYPE)
2. Create pl8_struct in tree-core.h
3. Parser support for pl8 literals
4. Type checking for pl8 operations