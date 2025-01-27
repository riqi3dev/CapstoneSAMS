import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import '../../../constants/Strings.dart';
import '../../../constants/theme/pallete.dart';
import '../SearchPatientDelegate.dart';

class SearchBarWidget extends StatefulWidget {
  const SearchBarWidget({
    super.key,
  });

  @override
  State<SearchBarWidget> createState() => _SearchBarWidgetState();
}

class _SearchBarWidgetState extends State<SearchBarWidget> {
  @override
  Widget build(BuildContext context) {
    final currentWidth = MediaQuery.of(context).size.width;
    final double minWidth = 150;
    final double maxWidth = 600;
    return Container(
      alignment: Alignment.center,
      child: GestureDetector(
        onTap: () {
          showSearch(
            context: context,
            delegate: SearchPatientDelegate(),
          );
        },
        child: ClipRRect(
          borderRadius: BorderRadius.circular(20),
          child: Container(
            width: currentWidth < 600 ? minWidth : maxWidth,
            height: 40,
            color: Pallete.lightGreyColor,
            child: SearchBarDesign(),
          ),
        ),
      ),
    );
  }

  Row SearchBarDesign() {
    return Row(
      children: [
        SizedBox(
          width: 15,
        ),
        FaIcon(
          FontAwesomeIcons.magnifyingGlass,
          size: 16,
          color: Pallete.greyColor,
        ),
        SizedBox(
          width: 5,
        ),
        Flexible(
          child: Text(
            Strings.searchAPatient,
            overflow: TextOverflow.ellipsis,
            style: TextStyle(
              fontSize: 18,
              color: Pallete.greyColor,
              fontWeight: FontWeight.normal,
            ),
          ),
        ),
      ],
    );
  }
}
