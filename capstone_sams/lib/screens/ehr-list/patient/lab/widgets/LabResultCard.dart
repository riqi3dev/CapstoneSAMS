import 'package:capstone_sams/models/LabResultModel.dart';
import 'package:flutter/material.dart';
import '../../../../../constants/theme/pallete.dart';
import '../../../../../constants/theme/sizing.dart';

class LabResultCard extends StatelessWidget {
  final Labresult labresult;
  final int a;
  LabResultCard({required this.labresult, required this.a});

  @override
  Widget build(BuildContext context) {
    final titles = ["TEST", '', "VALUE", "UNIT", "REFERENCE"];
    final array = labresult.jsonTables![a];
    final matrix = array['data'];

    return Container(
      margin: EdgeInsets.only(bottom: Sizing.sectionSymmPadding),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: <Widget>[
          Container(
            decoration: BoxDecoration(
              color: Pallete.mainColor,
              borderRadius: BorderRadius.only(
                  topRight: Radius.circular(Sizing.borderRadius),
                  topLeft: Radius.circular(Sizing.borderRadius)),
            ),
            alignment: Alignment.centerLeft,
            padding:
                EdgeInsets.symmetric(horizontal: Sizing.sectionSymmPadding),
            width: MediaQuery.of(context).size.width,
            height: Sizing.cardContainerHeight,
            child: Text(
              labresult.title,
              style: TextStyle(
                  color: Pallete.whiteColor,
                  fontSize: Sizing.header3,
                  fontWeight: FontWeight.w600),
            ),
          ),
          Container(
            decoration: BoxDecoration(
              color: Pallete.whiteColor,
            ),
            alignment: Alignment.centerLeft,
            padding: EdgeInsets.only(
                top: Sizing.sectionSymmPadding,
                left: Sizing.sectionSymmPadding,
                right: Sizing.sectionSymmPadding),
            width: MediaQuery.of(context).size.width,
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Comments: ',
                  style: TextStyle(
                      color: Pallete.textColor,
                      fontSize: Sizing.header6,
                      fontWeight: FontWeight.w600),
                ),
                Flexible(
                  child: Text(
                    labresult.comment,
                    style: TextStyle(
                        color: Pallete.textColor,
                        fontSize: Sizing.header6,
                        fontWeight: FontWeight.normal),
                  ),
                ),
              ],
            ),
          ),
          Expanded(
            child: Container(
              decoration: BoxDecoration(
                color: Pallete.whiteColor,
                borderRadius: BorderRadius.only(
                    bottomRight: Radius.circular(Sizing.borderRadius),
                    bottomLeft: Radius.circular(Sizing.borderRadius)),
              ),
              padding: const EdgeInsets.only(
                top: Sizing.sectionSymmPadding / 2,
                bottom: Sizing.sectionSymmPadding,
                left: Sizing.sectionSymmPadding,
                right: Sizing.sectionSymmPadding,
              ),
              child: SingleChildScrollView(
                physics: const BouncingScrollPhysics(),
                scrollDirection: Axis.vertical,
                child: SingleChildScrollView(
                  physics: const BouncingScrollPhysics(),
                  scrollDirection: Axis.horizontal,
                  child: DataTable(
                    columns: titles.map<DataColumn>((item) {
                      return DataColumn(label: Text(item));
                    }).toList(),
                    rows: matrix.map<DataRow>((row) {
                      return DataRow(
                        cells: row.map<DataCell>((cell) {
                          return DataCell(Text(cell['text'] ?? ''));
                        }).toList(),
                      );
                    }).toList(),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
