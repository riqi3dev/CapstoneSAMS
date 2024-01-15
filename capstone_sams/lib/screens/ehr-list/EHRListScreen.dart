import 'dart:math';
import 'package:capstone_sams/constants/Dimensions.dart';
import 'package:capstone_sams/constants/Strings.dart';
import 'package:capstone_sams/declare/ValueDeclaration.dart';
import 'package:capstone_sams/global-widgets/SearchAppBar.dart';
import 'package:capstone_sams/models/ContactPersonModel.dart';
import 'package:capstone_sams/models/PatientModel.dart';
import 'package:capstone_sams/providers/AccountProvider.dart';
import 'package:capstone_sams/providers/ContactPersonProvider.dart';
import 'package:capstone_sams/screens/ehr-list/widgets/PatientCard.dart';
import 'package:capstone_sams/screens/home/widgets/CourseDialog.dart';
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:provider/provider.dart';
import '../../constants/theme/pallete.dart';
import '../../constants/theme/sizing.dart';
import '../../providers/PatientProvider.dart';

class EhrListScreen extends StatefulWidget {
  @override
  State<EhrListScreen> createState() => _EhrListScreenState();
}

class _EhrListScreenState extends State<EhrListScreen> {
  late Stream<List<Patient>> patients;
  late String token;
  ScrollController _controller = ScrollController();
  String selectedPatientId = '';
  final double items = 24;
  final start = 0;
  int currentPageIndex = 0;
  int pageRounded = 0;
  double? totalPatients = 0;
  double pages1 = 0;

  @override
  void initState() {
    super.initState();
    token = context.read<AccountProvider>().token!;
    patients =
        Stream.fromFuture(context.read<PatientProvider>().fetchPatients(token));
  }

  void _scrollUp() {
    _controller.animateTo(
      _controller.position.minScrollExtent,
      duration: Duration(seconds: 1),
      curve: Curves.fastOutSlowIn,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      endDrawer: ValueDashboard(),
      appBar: PreferredSize(
        child: SearchAppBar(
            iconColorLeading: Pallete.whiteColor,
            iconColorTrailing: Pallete.whiteColor,
            backgroundColor: Pallete.mainColor),
        preferredSize: Size.fromHeight(kToolbarHeight),
      ),
      body: SingleChildScrollView(
        controller: _controller,
        padding: EdgeInsets.only(
          left: Sizing.sectionSymmPadding,
          right: Sizing.sectionSymmPadding,
          top: Sizing.sectionSymmPadding * 2,
          bottom: Sizing.sectionSymmPadding * 4,
        ),
        scrollDirection: Axis.vertical,
        physics: BouncingScrollPhysics(),
        child: StreamBuilder(
          stream: patients,
          builder: (context, snapshot) {
            List<Patient> dataToShow = [];
            if (snapshot.hasError) {
              return Center(
                child: Text('Error: ${snapshot.error}'),
              );
            } else if (snapshot.connectionState == ConnectionState.waiting) {
              return Center(
                child: const CircularProgressIndicator(),
              );
            } else if (snapshot.data!.isEmpty) {
              return Center(
                child: Text(Strings.noPatientResults),
              );
            } else if (snapshot.hasData) {
              dataToShow = snapshot.data!;
              final start = currentPageIndex * items.toInt();
              final end = min(
                  (currentPageIndex.toInt() * items.toInt()) + items.toInt(),
                  dataToShow.length);

              dataToShow = dataToShow.sublist(start, end);
              totalPatients = snapshot.data?.length.toDouble();
              pages1 = (totalPatients! / items);

              if (pages1 > items) pages1++;
              pageRounded = pages1.ceil();
            }

            return LayoutBuilder(
              builder: (BuildContext context, BoxConstraints constraints) {
                if (constraints.maxWidth >= Dimensions.mobileWidth) {
                  return _tabletView(dataToShow, start);
                } else {
                  return _mobileView(dataToShow, start);
                }
              },
            );
          },
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => showDialog(
          context: context,
          builder: (ctx) => CourseDialog(),
        ),
        child: FaIcon(
          FontAwesomeIcons.pencil,
        ),
      ),
      bottomNavigationBar: Padding(
        padding: EdgeInsets.symmetric(vertical: Sizing.spacing),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            ChevronPrev(),
            Text(
              '${currentPageIndex + 1} out of $pageRounded ',
            ),
            ChevronNext(),
          ],
        ),
      ),
    );
  }

  ElevatedButton ChevronPrev() {
    return ElevatedButton(
      onPressed: () => {
        _scrollUp(),
        if (currentPageIndex > 0)
          {
            setState(() {
              currentPageIndex -= 1;
            })
          }
      },
      child: const FaIcon(FontAwesomeIcons.chevronLeft),
      style: ElevatedButton.styleFrom(
        primary: Pallete.mainColor,
        elevation: 3,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(100.0),
        ),
        minimumSize: Size(50, 50),
      ),
    );
  }

  ElevatedButton ChevronNext() {
    return ElevatedButton(
      onPressed: () => {
        _scrollUp(),
        if (currentPageIndex < pageRounded - 1)
          {
            setState(() {
              currentPageIndex += 1;
            })
          }
      },
      child: const FaIcon(FontAwesomeIcons.chevronRight),
      style: ElevatedButton.styleFrom(
        primary: Pallete.mainColor,
        elevation: 3,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(100.0),
        ),
        minimumSize: Size(50, 50),
      ),
    );
  }

  GridView _mobileView(List<Patient> dataToShow, int start) {
    return GridView.builder(
      shrinkWrap: true,
      padding: EdgeInsets.only(),
      physics: const BouncingScrollPhysics(),
      itemCount: dataToShow.length,
      itemBuilder: (context, index) {
        final patient = dataToShow[index];
        final labresult = int.parse(patient.patientId as String);
        return PatientCard(
          patient: patient,
          onSelect: (patientId) {
            setState(() {
              selectedPatientId = patientId;
            });
          },
          labresult: labresult,
        );
      },
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 1,
        mainAxisSpacing: 10,
        crossAxisSpacing: 10,
        childAspectRatio: MediaQuery.of(context).size.width /
            (MediaQuery.of(context).size.height / 3.5),
      ),
    );
  }

  GridView _tabletView(List<Patient> dataToShow, int start) {
    return GridView.builder(
      shrinkWrap: true,
      physics: const BouncingScrollPhysics(),
      itemCount: dataToShow.length,
      itemBuilder: (context, index) {
        final patient = dataToShow[index];
        final labresult = int.parse(
          patient.patientId as String,
        );
        return PatientCard(
          patient: patient,
          onSelect: (patientId) {
            setState(() {
              selectedPatientId = patientId;
            });
          },
          labresult: labresult,
        );
      },
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        mainAxisSpacing: 10,
        crossAxisSpacing: 10,
        childAspectRatio: 16 / 10,
      ),
    );
  }
}
