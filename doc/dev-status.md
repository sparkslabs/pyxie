## Detailed Development status

The purpose of this page is for those who wonder "what's being
done/planned", either because they're just interested or potentially
interested in contributing.  That should explain the ordering.  Numbers have
no relevance, aside from to allow identification of a given task in git
commits. _(This is exported from trello)_

### Project Stage

* HEADLINE: PRE-ALPHA
* DEV STATE: WORKING (USABLE)
* DEV VERSION: 0.1.26
* RELEASED: 0.1.25 (2 Feb 2018)
* LANGUAGE STATE: BARE*
* FOCUS: Basic User Functions, Practicalities (Arduino Profile real example) - Get the Puppy/Kitten Robot working
* Newsletter created at http://tinyletter.com/sparkslabs


### WIP

* 297\. Detangle the code transforms out from the cppnodes...
* 18\. Code generation of C literals is muddled up a touch with structural representation #internals
* 293\. Extract the transforms from cppnodes into pyxie.transform.ii2cpp


### Paused



### Backlog: Arising

* 292\. Debian packaging should include examples
* 294\. Website should include examples.
* 295\. Move analysis to pyxie.transform.analysis


### Release Backlog: Features

* 0\.1.26 = = = = = = = = = =
* 286\. Revise iiNodes to use ECS like ideas
* 288\. Use ECS style iiNodes for type inference and variable collation
* 291\. Rename model.transform to transform.pynodetoiinode
* 32\. C Syntax Tree is a Tree #internals


### Release Backlog: Tasks

* 0\.1.26 - - - - - (tasks)
* 0\.1.25 - - - - - (tasks)
* 287\. Make repo more visible
* 57\. Blog post: Pyxie structure #website


### Known Bugs / Anti-features



### Backlog: Proposed Next

* 271\. Transformation from python AST to C-CST exists/works - for simplest possible function
* 268\. Code generation for very basic functions succeeds. (no args, return values or variables)
* 267\. Analysis of functions not using any variables succeeds (no args, no return values)
* 221\. Initial spike support for function definitions. (no args, no return values)
* 273\. Code generation for functions has cross overs for that of identifier definition.
* -----------------------------
* 223\. Spike support for functions with basic arguments.
* 222\. Spike support for functions which use local variables
* 251\. Profile Context is usable for defining externally defined methods (for typechecking)
* 227\. .get_type() should be delegated, not rely on internal pynode details.
* 15\. Refactor code generation #refactor #internals
* 16\. Find Variables duplicates effort from the analysis phase, while also relying on results from it #internals
* 17\. Transform step is throwing away data. This seems broken and should perhaps pass through decorated pynodes - or at least retain a reference. #internals
* 58\. Blog Post: Pyxie Decisions #website


### Backlog: Features

* 31\. Features focusses on BARE level functionality
* -----------------------------
* == NEED ======
* 38\. Generalise special casing of function calls. #practicalities
* 40\. Core expression code generation for strings #pylang
* 41\. Implement container oriented comparison operators  #pylang
* 42\. Implement identity oriented comparison operators  #pylang
* 48\. Modulo Operator for Integers #pylang
* -----------------------------
* == USEFUL ======
* 33\. Can find_variables(AST) in pyxie.model.transform actually just look in the results of the analysis phase? It should be able to. Building the same structure after all #internals
* 36\. Comments are implemented - would be useful for documented tests more appropriately #pylang
* 28\. Better Error messages for users #pylang #practicalties
* 14\. Code Cleanups #refactor #internals
* 4\. Compilation profiles are pluggable
* 13\. Pyxie compile harness supports custom working directories #practicalities
* 21\. Truthiness for values that AND/OR/NOT arguments needs resolving properly in C. (deferred) #pylang
* 22\. Truthiness of expressions is explicitly checked/valid - for us in if and while statements and boolean expressions #pylang #internals
* 47\. Modulo Operator for Strings #pylang
* -----------------------------
* == WANT ======
* Flesh out a micro:bit profile.
* 196\. Batch Compiler
* 197\. Web Editor
* 39\. Variables inside while loops are handled correctly #testing
* -----------------------------
* == WOULDLIKE ======
* 24\. Currently have 2 shift/reduce conflicts. They're auto-resolved correctly, but could be worth seeing if they could be resolved better. #pylang #internals
* 59\. Start thoughts on pyxie-web #reflect #website
* 9\. Add the manpage to the distributed files, into the right places #docs
* 8\. Add updating man page to the makefile #docs
* 11\. MBed compatible compilation profile? (Seeedstudio Arch)
* 12\. MSP430 compatible compilation profile?
* 25\. Consider using CppHeaderParser on the C++ side of things - to inform the code generation side of things #internals #pylang
* 259\. Would be nice to remove extraneous brackets round generated C++ expressions
* 27\. Operations and operators could be unified with a bit of tweaking - using "x.operation", not "x.tag/x.comparison" etc #internals #refactor
* 29\. Duplication exists within code generation for operators. (cf convert_operator etc) #internals #refactor
* 35\. Unify Boolean operator pynode implementations #refactor #internals
* 43\. Code generation for integer literals retains original representation where possible (Octal, hex, binary, etc) #practicalities
* 44\. Function call code supports C style function prototypes for type definitions #tbd
* 45\. Function call code supports name C headers for type definitions #tbd
* 46\. Pyxie caches results of C style header parsing #tbd
* 49\. Modulo Operator for Floats #pylang
* == NOT PRIORITISED ======


### Backlog: Tasks

* 52\. Review whether context should check types of ALL expressions, rather than just first, and whether we can should try to detect type mismatches #reflect
* 272\. Review Core Python Types To Do Next


### Backlog: Website, docs, etc

* 20\. Website side bar could be better implemented. #website
* 50\. Link current test programs on the website, maybe #website
* 232\. Would be nice to have a prettier website
* 23\. Website could do with some pictures :-) #website
* 233\. Some sort of Logo would be nice
* 60\. Start thoughts on pyxie-gui #reflect
* 30\. Should we allow comments on website? #website
* 19\. Website should use responsive CSS #website


### Features Implemented

* 296\. Remove a large chunk of old extraneous debugging output
* 290\. Rename "codegen" as "transform"
* 0\.1.25 = = = = = = = = = =
* 289\. Reimplement Cpp Operators
* 283\. Delete thunk
* 281\. Create classes for remaining iiNodes (if appropriate)
* 280\. Decorate CppNodes to use thunk to continue functioning using *either* iinodes or lists
* 282\. Shift code to use the actual iiNodes, removing use of thunk
* 279\. Create thunk that can take both iiNode lists or iiNodes to allow transition to iiNodes
* 278\. Create base class iiNode
* 285\. Document SemVer for Pyxie
* 284\. Create a pyxie.api import, to allow the use of Pyxie as an API.
* 277\. Move all creation of iiNode lists into functions in pyxie.models.iinodes
* 276\. Shift CppNodes into new location
* 275\. Rename existing CppNodes to make things clearer
* 274\. Create pyxie.models.cppnodes
* 0\.1.24 = = = = = = = = = =
* Prep Release 0.1.24
* 269\. Pynode support for def statements
* 270\. Add a callable type
* 266\. Grammar parsing for function definition succeeds
* 265\. Lexing for function definition succeeds
* 37\. Add special case for function calls like print... #pylang
* 34\. Function call code supports simplified type definitions for externals. #practicalities
* 26\. Block structure of generated C Code is pretty/human friendly/readable #internals
* 3\.5 Analysis code looks for an arduino profile file describing c-types appropriately.
* 3\.6 Arduino profile now configured in separate "profile" interface file
* 215\. v0 no funcs Playful Puppy code compiles, and runs on device correctly
* 214\. v0 no funcs Playful Puppy code generates code
* 213\. v0 no funcs Playful Puppy code analyses
* 264\. Check all Pynodes add all sub nodes as children correctly
* 263\. Bug: "elif" not analysing/generating code correctly regarding context
* 262\. BUGFIX: "else" not analysing/generating code correctly regarding context
* 195\. Functionality of bin/pyxie-dev is in core, not a script
* 0\.1.23 = = = = = = = = = =
* 258\. Improve Arduino profile documentation
* 260\. Arduino Profile supports HIGH,LOW,INPUT,OUTPUT,A0-A7
* 238\. Update grammar on website/in docs to match current grammar.
* 206\. Arduino profile supports millis()
* 241\. Arduino: Support "constrain"
* 242\. Arduino: Support "random"
* 247\. Arduino: Support "Serial.println"
* 243\. Arduino: Support "analogWrite"
* 246\. Arduino: Support "Serial.print"
* 244\. Arduino: Support "Serial" object
* 245\. Arduino: Support "Serial.begin"
* 240\. Arduino: Support arduino "map"
* 205\. Arduino: Support "analogRead"
* 257\. Arduino Analog sample compiles
* 256\. Arduino Analog sample analyses
* 3\.8 Arduino compiled programs can use values returned from functions.
* 250\. Profile Context is usable for defining external predefined/preinitialised variables
* 249\. Profile Context is usable for defining types of external identifiers
* 248\. Identifiers as rvalues should codegen as names not strings
* 255\. Arduino Analog sample parses
* 254\. Create Analog arduino sample
* 252\. MAJOR CHANGE print must be a function (to enable Serial.print to be valid syntax)
* 253\. FIXBUG: no default profile context breaks tests
* 259\. Update various statements on website about utility of Pyxie
* 0\.0.22 = = = = = = = = = =
* Add ability to control the arduino model building for
* 0\.0.21 = = = = = = = = = =
* 203\. Arduino profile supports delayMicroseconds
* 225\. Implementation of attribute access is sufficient for arduino profile.
* 210\. Parsing of Servo.writeMicroseconds() method call works as you'd expect
* 201\. Arduino profile supports Servos
* 230\. Implementation can generate code for myservo.attach(pin)
* 231\. PyAttribute(PyNode) needs to have a reference to the thing it's an attribute of when it's being accessed via PyAttributeAccess
* 229\. Implementation can analyse call to myservo.attach(pin)
* 0\.0.20 = = = = = = = = = =
* Subsume tree functionality into core
* Shorten names in profile definitions for clarity
* Better python 3 compatibility
* Experimental addition to look at name of thing, not value
* Use func_label to refer to the callable, not callable_
* Removed use of indenting logger :-)
* Add comment to indenting logger
* Changes to support debugging analysis
* Prettify generated C++ files
* Bump packaging for release
* 194\. Docs on pyxie-dev usage
* 0\.0.19 = = = = = = = = = =
* 207\. Arduino profile supports constants "HIGH", "LOW", "OUTPUT"
* 202\. Arduino profile supports digitalWrite
* 204\. Arduino profile supports pinMode
* 209\. Parsing of Servo.attach() method call works as you'd expect
* 226\. Implementation can analyse a simple call to arduino Servo() from Servo.h
* 228\. Compiler Runs under Python 3 (and Python 2)
* 0\.0.18 = = = = = = = = = =
* 224\. Parsing of attribute access is implemented
* 51\. Pyxie compile harness is switched over to use a better system for determining runtime options #internals
* 220\. range(start,end,step) is supported
* 218\. Method calls for objects can be parsed.
* 219\. Support for dumping the parse tree results as a json file.
* 200\. Pyxie can generate signed long values
* 199\. Pyxie can generate unsigned long values
* 217\. Code Generation understands what to do with LONG/UNSIGNED LONG values
* 216\. Pynodes exist for LONG/UNSIGNED LONG
* 211\. Negated expression like "-temp/2" are parsed and work
* 208\. Parsing of 0l and 0L works for unsigned and signed longs
* 198\. Pyxie Code for Playful Puppy Exists basic version
* 212\. Basic version of Playful Puppy code parses
* 0\.0.17 = = = = = = = = = =
* 193\. Update website to include the changes for 0.0.16/0.0.17 #docs
* 56\. Blog post: Introducing Pyxie #docs #website
* 3\.7.1 Integrate alternative generator/iterator protocol into compiler
* 3\.7 Arduino platform has alternative generator/exception implementation due to lack of exceptions
* pass statement
* 6\. Functionality of bin/pyxie is in core, not a script
* 0\.0.16 = = = = = = = = = =
* 3\. Arduino LEONARDO compatible compilation profile.
* 3\.3 Code generation outputs code targetting "setup" instead of "main"
* 3\.4 Makefile uses the arduino makefile #arduino leonardo
* 4\.1 compilation profiles support removal of elements of the clib
* 3\.2 Code generation is called with this switch toggled
* 3\.1 Detect that we are in a profile mode from a command line switch
* 2\. Function calls that do not require arguments are tested
* 61\. Make Release Script
* 62\. build_release_script.py
* 63\. Documentation in /docs is generated from website source documentation
* 64\. Docs on usage #docs
* 65\. Man page for pyxie
* 66\. Docs in README.md, setup.py and docs/ are generated from website.
* 67\. Support for for statements
* 0\.0.15 = = = = = = = = = =
* 71\. BUG: clibs can only be used on development machine...
* 0\.0.14 = = = = = = = = = =
* 74\. BUG: Putting the for loop at the end of the program causes compilation to fail
* 75\. BUG: statement_block at EOF not emitting dedents correctly #fixed
* 76\. Simple for...range loops
* 77\. Function call code supports simplified type definitions for builtins (such as range)
* 78\. Compile phase is split into "codegen" and "compile"
* 79\. Implement a simple iterator protocol for C++ objects - to allow implementation of something like range functions and generators.
* 80\. Implementation of a simple C Library to include into user generated code as necessary.
* 0\.0.13 = = = = = = = = = =
* 82\. Parsing bracketed full expressions
* 83\. Chained boolean expressions and chained mixtures of boolean expressions work as expected
* 84\. Boolean expression support: NOT
* 85\. Boolean expression support: AND
* 86\. Boolean expression support: OR
* 87\. Support for if/elif/else statements
* 88\. Support for if statements
* 0\.0.12 = = = = = = = = = =
* 92\. Release tasks: 0.0.12
* 93\. Comparison operators
* 94\. Can now handle loops that count towards zero and do something with them...
* 95\. support for while statements
* 96\. While Loop conditional is a expression
* 97\. Continue works in a While loop
* 98\. Break works with With True
* 99\. While works with While True:
* 100\. Define basic principles for Pyxie
* 0\.0.11 = = = = = = = = = =
* 108\. Function call code generation supports Print as special case
* 109\. Code generation function calls
* 110\. Support python comments so we can CHEAT and do things like #include <arduino.h> :-D (What a *neat* idea :-) )
* 111\. Parsing function calls
* 0\.0.10 = = = = = = = = = =
* 115\. Pyxie will now compile files outside the pyxie code tree
* 116\. Code generation of expression statements.
* 117\. Test suite checks that programs that should fail to compile do so
* 118\. Test suite uses new analysis hook
* 119\. PARSING USES STANDARD TREE MODEL, BUT ALSO USES CUSTOM TRAVERSALS FOR FLEXIBILITY
* 120\. Type inference code changes are refactored and cleaned up
* 121\. Strategy for managing variables needs defining
* 122\. New strategy for type inference - lexical scope friendly
* 123\. Analysis through tree for identifiers doesn't work as expected. Needs fixing/resolving
* 124\. Now, before we analyse types, all identifiers are guaranteed to be in the global context. We don't need to stuff in a new version, just update it.
* 125\. Contexts themselves are kinda wrong, need a rethink
* 126\. Analysis Phase adds context
* 127\. Pynodes are tree nodes (and hence trees)
* 128\. Analyse is an explicit phase internally, initially focussed on types
* 129\. Results of analyse phase can be made visible.
* 130\. Docs added to pyxie/__init__.py
* 0\.0.9 = = = = = = = = = =
* 139\. Pyxie harness supports parsing random files
* 140\. Pyxie harness supports compiling random files
* 141\. Pyxie harness has a testing mode
* 142\. Bracket negative literal values in expressions to avoid confusing C++
* 145\. Pyxie is now left recursive not right recursive
* 146\. conversion of expression statements
* 147\. BUG: 10-1-2 gives 9 not 11
* 0\.0.8 = = = = = = = = = =
* 151\. Replace python AST list style representation with a nodal representation - to simplify type decoration etc
* 152\. Type inference for expressions
* 153\. assignment where the rvalue is a simple integer expression
* 154\. Variable types are looked upin/stored to  a global context.
* 155\. Testcase added for assignments where the rvalue is an expression
* 156\. BUGFIX: Should only include iostream once, if at all.
* 157\. Printing of op_func blocks
* 158\. Conversion of core "operator functions" for integers
* 159\. Code generation for INTEGER core expressions
* 160\. BUGFIX: Precedence for operators is inverted for some reason.  +- binding tighter than */
* 161\. BUG - When the parser is reused, line numbers in lexer do not reset for new files
* 162\.Parsing core expressions - times, divide, power, plus, minus  - NOT function call, not parenthesised
* 163\. Parsing blocks generates block tokens
* 164\. Lexical Analysis matches initial language spec
* 165\. Print handles mixed literals
* 166\. Code generation for atomic literals
* 167\. "models" contains an initial baseline model mapping python-CST to CPP-CST
* 168\. Generation of decorated CPP-CST from parsed assignment statements
* 169\. C++ Code can be generated from the baseline CPP-CST for libc based testing
* 170\. Parsing assignment statements
* 171\. Parsing identifiers
* 172\. Parsing of value literals
* 173\. Baseline parser/lexer infrastructure for parser build/testing
* 174\. Long description on PyPI


### Tasks Done

* 0\.1.23 - - - - - (tasks)
* 0\.1.23 Release tasks
* 0\.0.22 - - - - - (tasks)
* 239\. 0.0.22 Release tasks
* 0\.0.22 - - - - - (tasks)
* 239\. 0.0.21 Release tasks
* 0\.0.20 - - - - - (tasks)
* Update changelog
* Add newsletter subscription to site info
* 234\. Replicate *target* release issues for 0.0.20 into github
* 235\. Newsletter for sparkslabs projects exists.
* 236\. Re-order trello lists by left to right order to make more usable
* 237\. Tweak git repo
* 0\.0.19 - - - - - (tasks)
* 0\.0.18 - - - - - (tasks)
* Package for release and release (DONE)
* Cleanup clib packaging
* 0\.0.17 - - - - - (tasks)
* 10\. Decide whether to add functionality of bin/pyxie-dev is in core
* 0\.0.16 - - - - - (tasks)
* 1\. Number Cards in backlog.
* 7\. For Release: 0.0.16
* 192\. Trello snapshot generation escapes task numbers.
* 68\. Write Bump Versions Script.
* 69\. Re-prioritise backlog for 0.0.16
* 70\. Breakdown features needed for a release script
* 0\.0.15 - - - - - (tasks)
* 72\. For Release: 0.0.15
* 73\. Bump Versions
* 0\.0.14 - - - - - (tasks)
* 81\. For Release: 0.0.14
* 0\.0.13 - - - - - (tasks)
* 89\. For Release: 0.0.13
* 90\. Decide on Python Modulo operator?
* 91\. Bump Versions
* 0\.0.12 - - - - - (tasks)
* 101\. Update language status for 0.0.12
* 102\. BUG: Parser generates far too many "empty statements"
* 103\. Update language status for 0.0.11
* 104\. Check docs in pyxie/__init__.py match 0.0.12 Release
* 105\. Bump Versions
* 106\. Push rebased site to github/live
* 107\. Site for Pyxie, should link to language spec -- http://www.sparkslabs.com/Pyxie/language-spec.md
* 0\.0.11 - - - - - (tasks)
* 112\. For release: 0.0.11
* 113\. Check docs in pyxie/__init__.py match 0.0.11 Release
* 114\. Bump Versions
* 0\.0.10 - - - - - (tasks)
* 131\. For release: 0.0.10
* 132\. Check that programs that compile produce expected code
* 134\. Check docs in pyxie/__init__.py match 0.0.10 Release
* 135\. Update test target in makefile to match new pyxie args
* 136\. Bump Versions
* 137\. Order of functions in pynode matches grammar - making it easier to follow
* 138\. Document current parsing status more accurately
* 0\.0.9 - - - - - (tasks)
* 148\. Check that debian package being built/created does actually contains what's wanted
* 149\. Check that the tar ball being built/created for pypi actually contains what you want
* 150\. Version number bumped
* 0\.0.8 - - - - - (tasks earlier)
* 175\. Why the project doesn't use the standard python compiler/AST module
* 176\. Break down language features into specific feature tasks - for initial feature set
* 177\. pyxie compiler now accepts runtime options to control what tests get compiled
* 178\. Changelog for initial releases
* 179\. Initial language spec
* 180\. Packaging for pypi exists
* 181\. Packaging via PPA exists
* 182\. The CST for baseline Python code is simplified
* 183\. Initial testing infrastructure in place
* 184\. Private github repo for Pyxie
* 185\. initial README for Pyxie
* 186\. Pyxie 0.0.1 Released
* 187\. Pyxie 0.0.2 Released
* 188\. Pyxies 0.0.3 Released
* 189\. Pyxie 0.0.4 Released
* 190\. Pyxie 0.0.5 Released
* 191\. Bump Versions


### Pinned

* Things to feed into Pyxie
* Licensing links
* .p files are parsing tests. If they compile, they should be renamed .pyxie which are compilation tests.
* How to deploy the website
* Release tasks


### Rejected

* 54\. Review pypi packaging for things we should be doing - Seems OK for now
* 55\. Create pyxie-service for managing batch compilation services - to be folded into Make a Batch Compiler
* 53\. Use https://travis-ci.org/ - No time to do at the moment
* 261\. Consider PEP 484 based type hints - maybe later, but part of point of pyxie is to autodetect types
* 298\. Generated C++ code should a list of fragments and joined at the end.


