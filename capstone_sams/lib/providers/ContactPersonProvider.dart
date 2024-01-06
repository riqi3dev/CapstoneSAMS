import 'dart:convert';

import 'package:capstone_sams/constants/Env.dart';

import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;

import '../models/ContactPersonModel.dart';

class ContactPersonProvider extends ChangeNotifier {
  ContactPerson? _contactPerson;
  ContactPerson? get contactPerson => _contactPerson;
  String? get id => _contactPerson?.contactId;
  String? get fullName => _contactPerson?.fullName;
  String? get phone => _contactPerson?.phone;
  String? get address => _contactPerson?.address;
  String? get patientID => _contactPerson?.patient;

  var data = [];
  List<ContactPerson> _contactPeople = [];

  List<ContactPerson> get contactPeople => _contactPeople;

  Future<ContactPerson> fetchContactPeople(
      String token, String? patientID) async {
    print('provider${patientID}');
    final header = <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
      'Authorization': 'Bearer $token',
    };
    try {
      final response = await http.get(
          Uri.parse('${Env.prefix}/patient/patients/contact/${patientID}'),
          headers: header);
      await Future.delayed(Duration(milliseconds: 3000));
      if (response.statusCode == 200) { 
        return ContactPerson.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
      } else {
        return throw Exception('Failed to load contacts');
      }
    } on Exception catch (e) {
      return throw Exception('Failed to load contacts');
    }
  }
}