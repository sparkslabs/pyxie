---
template: mainpage
source_form: markdown
name: Language Spec
updated: July 2015 (partially with release 0.0.14)
title: Language Spec for Pyxie
---
## Little Python Language Spec

Little Python is a restricted subset of Python 3. (and 2.7)

**This is a work in progress.** The implementation does not yet match
this spec. As a result, the grammar will be slightly bogus. You hopefully
get the idea though.


## Semi-formal syntactic language features todo:

{% target_types = panel("panels/target-types.md") %}
{% target_lexical_analysis = panel("panels/target-lexical-analysis.md") %}
{% target_grammar = panel("panels/target-grammar.md") %}
<hr>
## Practical Details

{% cpp_integration = panel("panels/c++-integration.md") %}
{% lexical_states = panel("panels/lexical-analysis-states.md") %}

<hr>

{% todo_list = panel("panels/informal-todo-list.md") %}
{% to_not_do_list = panel("panels/informal-to-not-do-list.md") %}
{% to_maybe_do_list = panel("panels/informal-to-maybe-do-list.md") %}
