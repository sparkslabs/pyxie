---
template: mainpage
source_form: markdown
name: Project Status
updated: July 2015 (with release 0.0.14)
title: Project Status (overview)
---
## Project Status

{% project_stage = panel("panels/trello-cardlist-project-stage.md") %}

### Dev states:

Overall standard ethos:

* Make it work
* Make it correct
* Make it fast

### Target Language states

* BARE-LEVEL - does the absolute minimum to be useful
* USABLE - does just that little bit more that you'd expect to work
* USABLE_CONTAINERS - includes some level of support for lists/dictionaries
* BETTER - sufficient for actually being useful in doing things with an arduino, mbed or MSP430 - should include mappings between "import" and "include" - even just basic ones.
* USER FUNCTIONS - As the name says, should support user functions
* CLASSES - Should support user classes
* SELF-HOSTED - Ambitious - should become self-hosted - implies ability to compile something similar to PLY, even simplified. This would gain speed.

{% guiding_principles = panel("panels/guiding-principles.md") %}
