 
import 'package:flutter/material.dart';

import '../../constants/theme/pallete.dart';

class ShortTextfield extends StatelessWidget {
  const ShortTextfield({
    super.key,
    required this.controller,
    required this.validator,
    required this.hintText,
  });

  final TextEditingController controller;
  final String validator, hintText;

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      validator: (value) => value == '' ? validator : null,
      decoration: InputDecoration(
        hintText: hintText,
        filled: true,
        fillColor: Pallete.palegrayColor,
      ),
    );
  }
}

// ignore: must_be_immutable
class TextAreaField extends StatelessWidget {
  TextAreaField({
    super.key,
    required this.validator,
    required this.hintText,
    required this.onSaved,
  });

  final String validator, hintText;
  String? onSaved;

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      keyboardType: TextInputType.multiline,
      minLines: 5,
      maxLines: null,
      onChanged: (value) => onSaved = value,
      validator: (value) => value == '' ? validator : null,
      decoration: InputDecoration(
        hintText: hintText,
        filled: true,
        fillColor: Pallete.palegrayColor,
        enabledBorder: OutlineInputBorder(
          borderSide: BorderSide(
            width: 1,
            color: Pallete.greyColor,
          ),
        ),
        focusedBorder: OutlineInputBorder(
          borderSide: BorderSide(
            width: 1,
            color: Pallete.mainColor,
          ),
        ),
      ),
    );
  }
}

class PasswordTextfield extends StatelessWidget {
  const PasswordTextfield({
    super.key,
    required this.controller,
    required this.validator,
    required this.hintText,
  });

  final TextEditingController controller;
  final String validator, hintText;

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      obscureText: true,
      validator: (value) => value == '' ? validator : null,
      decoration: InputDecoration(
        hintText: hintText,
        filled: true,
        fillColor: Pallete.palegrayColor,
      ),
    );
  }
}
