---
Summary: My take on semantic versioning and Pyxie
Updated: January 2017
Started: November 2016
Version: 0.1.24
Author: Michael Sparks
---
# What does Pyxie's Version Mean?

Pyxie's public released version as of today is 0.1.24.  This does actually
have some measure of meaning because it's based on semantic versioning
as defined at http://semver.org


## MAJOR.MINOR.RELEASE *not* MAJOR.MINOR.PATCH

SEMVER normally uses the form MAJOR.MINOR.PATCH, I use MAJOR.MINOR.RELEASE

The following is a sample release schedule used below.

* 0.5.56 - last dev release before 1.x.x release
* 1.6.57 - First stable 1.x.x release
* 0.6.58 - First dev release after 1.6.57, continuing development, adding new features
* 0.6.59 - Next dev release adding new features
* 0.7.60 - Next dev release adding new features
* 0.7.61 - Next dev release fixing bugs
* 1.7.62 - Second stable 1.x.x release
* 0.7.63 - Next dev release fixing bugs
* 0.7.64 - Next dev release adding features
* 0.8.65 - Next dev release adding major functionality
* 0.9.65 - Next dev release adding more major functionality
* 0.9.66 - Next dev release - candidate stable release perhaps.
* 2.9.67 - This stable release - adds major functionality, but in a
           backwards incompatible fashion, so MAJOR version bumps.


## Key principles

Given: MAJOR.MINOR.RELEASE
For all releases:

* **RELEASE** always increments over time with no branching. (This should
  be visible above). It means the code has changed and there's a reason
  for it! (features/bugs/docs/etc)

* **MINOR** always increases. This is a slightly odd choice, but the intent
      here is that MINOR is a measure of total project status/complexity.

* **MAJOR** = 0 --> dev release - always remains zero

* **MAJOR** > 0 --> non-dev release - only ever increases when there are
      backwards incompatible releases.
* Dev and non-dev releases may follow each other as per the slightly
      unusual release schedule described above.

For non-dev releases:

* No suprises when installing a release where MAJOR is unchanged.

* Where MAJOR.MINOR are unchanged it should not affect a user negatively.

* Installing a release where MINOR changes should contain a benefit
  such as major bug fixes or extra features

* Backwards incompatible changes must bump the MAJOR number.

* The MAJOR number *may* change where there are significant benefits
  over the previous first MAJOR release. (eg after many minor
  releases perhaps)

* Version numbers must be compatible with semantic versioning

* The API the release relates to must be clearly defined:
  - If it's not in the API docs, it isn't part of the release,
    and is subject to change.

* non-dev releases may be alpha or beta releases, and this is not
      as yet encoded in the version number

For dev releases:

* If MAJOR.MINOR has changed, then there is new major or breaking
  functionality.

* Otherwise, while not required, it is *likely* compatible with a
  previous version with the same MAJOR/MINOR number. Note that it
  is a dev release, this is not required.


## How this applies to Pyxie


### Current meaning of 0.1.24 -- as it applies to pyxie

Given 0.1.24 stands for MAJOR.MINOR.RELEASE, it means the following:

* MAJOR - 0 - This means that I view Pyxie as still in it's initial
  development phase.  ie the code it compiles looks increasingly python
  like - and is a valid subset of python, but doesn't really have the
  language coverage you would expect of a 1.x.x release.

* MINOR - 1 - If this was 0, it would mean that pretty much all bets are off
  about internal structure, and external API.  For this to bump to 1 it
  means that Pyxie is actually useful now for *something*.  In particular,
  at present, you can use it right now for controlling simple quadruped
  robots with sensors.

* RELEASE - 24 - This is literally a release number.  It means that this is
  the 24'th release of the codebase.


### Current meaning of 0.MINOR.RELEASE

Until I hit a 1.x.x release, these numbers will increase as follows:

* MAJOR - 0 - This will be 0 until I hit a 1.x.x release.  See the next
  section for criterion I have for this.

* MINOR - MINOR level versions are guaranteed to increase permanently and
  not reset to zero.  This will increment for one or both of the following
  reasons:
  - The language as implemented gains a major piece of practical
    functionality
  - The external API (command line) changes in an incompatible manner to the
    previous release.  (If things are simply *added* this will probably
    not change)

* RELEASE - This will be incremented for every release.  The change may be
  small or it may be large.  PATCH level versions are guaranteed to increase
  permanently and not reset to zero.


### Current meaning of 1.MINOR.RELEASE

Eventually I will hit a 1.x.x release, at which point this section applies.


### 1.x.x criterion

The criterion I have in mind follow.  These may change.  If so this will be
made clear below.  Specifically I would expect (at minimum) the following
features to be implemented.

Definitely:

* Lists
* Dictionaries
* Strings
* Simple user functions
* Tested with arduino profile

Maybe:

* Simple user classes (maybe)
* Tested with a micro:bit profile (maybe - very much a personal would like)

This list excludes the ones that have been done, so this list will hopefully
get shorter, not longer.


### Initial 1.x.x version

The initial version of 1.x.x will NOT be 1.0.0.

If the last release *before* the 1.x.x release was (for example) 0.5.56,
then the first 1.x.x release would either be 1.5.57 or 1.6.57

This is a natural consequence of the fact that MINOR always increases, and
only does as per rules above.  It's also a consequence of the fact that the
RELEASE number always increases.


### Releases after 1.x.x

After the first 1.x.x release, the project will use the core rules of
semantic versioning which are but modified slightly:

*Given a version number MAJOR.MINOR.PATCH, increment the:*

* *MAJOR version when you make incompatible API changes*
* *MINOR version when you add functionality in a backwards-compatible manner*
* *PATCH version for every release.  If just the PATCH version changes, it means bug fixes.*

(This differs from slightly Semver, but keeps the ordering guarantees, but
it also keeps concepts about history intact)

So to be clear:

* If MAJOR changes from 1 to 2, it means there are changes which are not
  backwards compatible.  This could include changes to the language.  Such
  versions will obviously be clearly flagged.
* If MINOR changes, it means there's new functionality.  In particular, if
  there were two versions 1.7.x and 1.9.x, then code developed for 1.7.x
  should work with 1.9.x.  However code developed for 1.9.x may not work
  with 1.7.x


### Parallel Releases

It's possible at some later point in time there may be parallel releases.

For example there may be a 0.5.56 and a 1.6.57 release.  It might be that
testing of an ideas and implementations continues in the 0.X.X release
chain.  (Reasoning: 0.x.x is considered unstable by definition)

This naturally also leads to the concepts of stable releases and unstable
releases.

This means the release schedule *could* be:

* 0.5.56 - last dev release before 1.x.x release
* 1.6.57 - First stable 1.x.x release
* 0.6.58 - First dev release after 1.6.57, continuing development, adding new features
* 0.6.59 - Next dev release adding new features
* 0.7.60 - Next dev release adding new features
* 0.7.61 - Next dev release fixing bugs
* 1.7.62 - Second stable 1.x.x release
* 0.7.63 - Next dev release fixing bugs
* 0.7.64 - Next dev release adding features
* 0.8.65 - Next dev release adding major functionality
* 0.9.65 - Next dev release adding more major functionality
* 0.9.66 - Next dev release - candidate stable release perhaps.
* 2.9.67 - This stable release - adds major functionality, but in a
           backwards incompatible fashion, so MAJOR version bumps.

*(Remember, the above is hypothetical!)*

This actually then maintains the ordering guarantees, and also allows people
to track the relationship of releases to dev releases, and how each release
relates to both previous stable releases *and* development releases.

Specifically, the stable releases would look like this:

* 1.6.57 - First stable 1.x.x release
* 1.7.62 - Second stable 1.x.x release
* 2.9.67 - This stable release - adds major functionality, but in a
           backwards incompatible fashion, so MAJOR version bumps.

Note that this maintains the strict ordering requirement we want/need.

The dev releases would look like this:

* 0.5.56 - last dev release before 1.x.x release
* 0.6.58 - First dev release after 1.6.57, continuing development, adding new features
* 0.6.59 - Next dev release adding new features
* 0.7.60 - Next dev release adding new features
* 0.7.61 - Next dev release fixing bugs
* 0.7.63 - Next dev release fixing bugs
* 0.7.64 - Next dev release adding features
* 0.8.65 - Next dev release adding major functionality
* 0.9.65 - Next dev release adding more major functionality
* 0.9.66 - Next dev release - candidate stable release perhaps.

Note again, that this maintains the strict ordering requirement we want/need.


### YAGNI?

This could seem like thinking things through too much, and "You Ain't Gonna
Need It".  In a way that's potentially true.

However, version numbers are essential for signalling to users of a package
the status, and they're also vital for package managers to  manage clearly
which version supercedes another.  You also do not want a user to
accidentally use an unstable version.

Also, to be fair, this is the sort of thinking I've had in my head for
versioning based on semver for a while, so writing it down seemed like a
good idea.  At some point it might be necessary to change this.

