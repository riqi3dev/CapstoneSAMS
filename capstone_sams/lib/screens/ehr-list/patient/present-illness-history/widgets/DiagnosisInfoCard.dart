import 'package:capstone_sams/constants/Strings.dart';
import 'package:capstone_sams/constants/theme/pallete.dart';
import 'package:capstone_sams/constants/theme/sizing.dart';
import 'package:capstone_sams/global-widgets/cards/CardSectionInfoWidget.dart';
import 'package:capstone_sams/global-widgets/cards/CardSectionTitleWidget.dart';
import 'package:capstone_sams/global-widgets/cards/CardTemplate.dart';
import 'package:capstone_sams/global-widgets/cards/CardTitleWidget.dart';
import 'package:capstone_sams/global-widgets/texts/NoDataTextWidget.dart';
import 'package:capstone_sams/models/AccountModel.dart';
import 'package:capstone_sams/models/PatientModel.dart';
import 'package:capstone_sams/models/PrescriptionModel.dart';
import 'package:capstone_sams/models/PresentIllness.dart';
import 'package:capstone_sams/providers/AccountProvider.dart';
import 'package:capstone_sams/providers/PresentIllnessProvider.dart';
import 'package:capstone_sams/screens/ehr-list/patient/present-illness-history/widgets/crud/ViewIllnessScreen.dart';
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:provider/provider.dart';

// ignore: must_be_immutable
class DiagnosisInfoCard extends StatefulWidget {
  final Patient patient;
  DiagnosisInfoCard({
    super.key,
    required this.patient,
  });

  @override
  State<DiagnosisInfoCard> createState() => _DiagnosisInfoCardState();
}

class _DiagnosisInfoCardState extends State<DiagnosisInfoCard> {
  late Stream<List<PresentIllness>> presentIllness;
  late String token = context.read<AccountProvider>().token!;

  @override
  void initState() {
    super.initState();

    token = context.read<AccountProvider>().token!;
    presentIllness = Stream.fromFuture(context
        .read<PresentIllnessProvider>()
        .fetchComplaints(token, widget.patient.patientID));
  }

  @override
  Widget build(BuildContext context) {
    AccountProvider accountProvider = Provider.of<AccountProvider>(context);

    String middleInitial = accountProvider.middleName![0];

    return CardTemplate(
      column: Column(
        children: [
          CardTitleWidget(
              title:
                  'Dr. ${accountProvider.firstName} ${middleInitial}. ${accountProvider.lastName}'),
          CardSectionTitleWidget(title: "Patient's Present Illnesses"),
          CardSectionInfoWidget(
            shader: true,
            widget: PresentIllnessData(),
          ),
        ],
      ),
    );
  }

  StreamBuilder<List<PresentIllness>> PresentIllnessData() {
    return StreamBuilder(
      stream: presentIllness,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return Center(child: CircularProgressIndicator());
        } else if (snapshot.hasError) {
          return Text('${snapshot.error}');
        } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return Center(
            child: Container(
              height: 100,
              child: Center(
                child: NoDataTextWidget(
                  text: Strings.noRecordedIllnesses,
                ),
              ),
            ),
          );
        } else {
          final presentIllnessList = snapshot.data!;

          return ListView.builder(
            shrinkWrap: true,
            physics: BouncingScrollPhysics(),
            itemCount: presentIllnessList.length,
            itemBuilder: (context, index) {
              final illness = presentIllnessList[index];
              final illnessIndex = '${presentIllnessList.length - index}';

              return Card(
                color: Colors.white,
                elevation: Sizing.cardElevation,
                margin: EdgeInsets.symmetric(
                  vertical: Sizing.sectionSymmPadding / 4,
                ),
                child: GestureDetector(
                  onTap: () =>
                      viewIllnessMethod(context, illness, illnessIndex),
                  child: ListTile(
                    title: Row(
                      children: [
                        Text(
                          'Dx #${illnessIndex}: ',
                        ),
                        Text(
                          '${illness.illnessName}',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '${illness.created_at}',
                          // style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                    trailing: popupActionWidget(illness, illnessIndex),
                  ),
                ),
              );
            },
          );
        }
      },
    );
  }

  PopupMenuButton<dynamic> popupActionWidget(
      PresentIllness illness, String illnessIndex) {
    return PopupMenuButton(
      itemBuilder: (context) => [
        PopupMenuItem(
          child: ListTile(
            leading: FaIcon(
              FontAwesomeIcons.solidEye,
              color: Pallete.infoColor,
            ),
            title: Text(
              'View',
              style: TextStyle(
                fontWeight: FontWeight.w700,
                color: Pallete.infoColor,
              ),
            ),
            onTap: () {
              viewIllnessMethod(context, illness, illnessIndex);
            },
          ),
        ),
        PopupMenuItem(
          child: ListTile(
            leading: FaIcon(
              FontAwesomeIcons.pen,
              color: Pallete.successColor,
            ),
            title: Text(
              'Edit',
              style: TextStyle(
                fontWeight: FontWeight.w700,
                color: Pallete.successColor,
              ),
            ),
            onTap: () {},
          ),
        ),
        PopupMenuItem(
          child: ListTile(
            leading: FaIcon(
              FontAwesomeIcons.trash,
              color: Pallete.dangerColor,
            ),
            title: Text(
              'Delete',
              style: TextStyle(
                fontWeight: FontWeight.w700,
                color: Pallete.dangerColor,
              ),
            ),
            onTap: () {},
          ),
        ),
      ],
    );
  }

  void viewIllnessMethod(
      BuildContext context, PresentIllness illness, String illnessIndex) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => ViewIllnessScreen(
            presentIllness: illness, illnessIndex: illnessIndex),
      ),
    );
  }

  PopupMenuButton<dynamic> nurseAction(
    int index,
    List<Prescription> prescriptionList,
    Prescription prescription,
  ) {
    return PopupMenuButton(
      itemBuilder: (context) => [
        PopupMenuItem(
          child: ListTile(
            leading: FaIcon(
              FontAwesomeIcons.pills,
              color: Pallete.infoColor,
            ),
            title: Text(
              'Manage',
              style: TextStyle(
                fontWeight: FontWeight.w700,
                color: Pallete.infoColor,
              ),
            ),
            onTap: () {},
          ),
        ),
      ],
    );
  }
}