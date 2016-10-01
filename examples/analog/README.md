Analog Example
--------------

Spelling note: this is spelt analog, rather than analogue because that's the
spelling in the API. I normally prefer UK spellings for things for obvious
reasons, but in this case consistency makes sense.

The purpose of this example is to provide a practical test for creating and
testing the following API and language elements:

   * Support for profile defined variables - such as A0
   * Support for profile defined objects - such as Serial
   * Support for proifle defined functions - such as analogRead, analogWrite

Furthermore it (unintentionally) caused the need to turn "print" from being a
separate syntactic value to being a function. This is necessary to support
things like Serial.print. This is a little frustrating because I'd hoped to
deal with this later, but it's such an important change, it needs to happen
sooner rather than later.

Current issues:

* print is not a function, but a syntactic structure. This causes
  Serial.print to be invalid syntax.

* We can define variables like A0 in the profile context, but it is
  currently generating a *string* "A0" in the generated code. This
  is unintentional and undesirable.

* It would be nice to not generate extraneous brackets around expressions
  if we could avoid it.

Positive points:

* If we change print to _print, code is generated. In the output code,
  if we manually change _print to print, the build succeeds.

* If we change in the generated code the strings incorrectly generated,
  that is "A0" to Ao - then the build succeeds.

This suggests that the code changes required for analysis are minimal,
which is something.


