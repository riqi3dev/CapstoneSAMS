import 'package:capstone_sams/providers/MedicalNotesProvider.dart';

import 'package:flutter/material.dart';

import 'package:capstone_sams/models/MedicalNotesModel.dart';
import 'package:capstone_sams/providers/AccountProvider.dart';

import 'package:provider/provider.dart';

import '../../../constants/theme/pallete.dart';
import '../../../constants/theme/sizing.dart';

class NotesSection extends StatelessWidget {
  NotesSection({
    Key? key,
    required this.title,
    required this.press,
    required this.todosPreview,
  }) : super(key: key);

  final String title;
  late final dynamic press;
  final List<Todo> todosPreview;

  @override
  Widget build(BuildContext context) {
    final username = context.watch<AccountProvider>().username;
    final totalTodos = context.watch<TodosProvider>().todos.length;
    int numTodos = todosPreview.length;
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.only(
            left: Sizing.sectionSymmPadding + 10,
            right: Sizing.sectionSymmPadding + 10,
            top: Sizing.sectionSymmPadding + 10,
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Flexible(
                child: Text(
                  'Your Notes',
                  overflow: TextOverflow.ellipsis,
                  style: TextStyle(
                    color: Pallete.textColor,
                    fontSize: Sizing.header4,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
              TextButton(
                onPressed: press,
                child: Text(
                  'See All',
                  style: TextStyle(
                    color: Pallete.mainColor,
                  ),
                ),
              ),
            ],
          ),
        ),
        GestureDetector(
          onTap: press,
          child: Padding(
            padding: const EdgeInsets.symmetric(
                horizontal: Sizing.sectionSymmPadding),
            child: Card(
              elevation: Sizing.cardElevation,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(Sizing.roundedCorners),
              ),
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(Sizing.roundedCorners),
                  color: Pallete.whiteColor,
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.1),
                      spreadRadius: 2,
                      blurRadius: 5,
                      offset: Offset(0, 3),
                    ),
                  ],
                ),
                padding: const EdgeInsets.all(Sizing.sectionSymmPadding * 1.5),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          '$username\'s Notes',
                          overflow: TextOverflow.ellipsis,
                          style: TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 18,
                          ),
                        ),
                        // Text(
                        //   '$totalTodos targets to do',
                        //   style: TextStyle(
                        //     color: Pallete.textColor,
                        //     fontSize: 12,
                        //   ),
                        // ),
                        Text(
                          '$numTodos ${numTodos == 1 ? 'target out of $totalTodos' : 'targets out of $totalTodos'}',
                          style: TextStyle(
                            color: Pallete.textColor,
                            fontSize: 12,
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 10),
                    ...todosPreview
                        .map((todo) => TodoCard(
                              todo: todo,
                              token: context.read<AccountProvider>().token!,
                            ))
                        .toList(),
                  ],
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}

class TodoCard extends StatefulWidget {
  final Todo todo;
  final String token;

  const TodoCard({required this.todo, required this.token});

  @override
  _TodoCardState createState() => _TodoCardState();
}

class _TodoCardState extends State<TodoCard> {
  bool isDone = false;

  @override
  void initState() {
    super.initState();
    isDone = widget.todo.isDone;
  }

  @override
  Widget build(BuildContext context) {
    final accountID = context.read<AccountProvider>().id;
    return Card(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                Checkbox(
                  activeColor: Pallete.mainColor,
                  checkColor: Colors.white,
                  value: isDone,
                  onChanged: (newValue) {
                    setState(() {
                      isDone = newValue!;
                    });
                    final provider =
                        Provider.of<TodosProvider>(context, listen: false);
                    provider.toggleTodoStatus(
                        widget.todo, accountID!, widget.token);
                  },
                ),
                const SizedBox(width: 8),
                Text(
                  widget.todo.title,
                  style: TextStyle(
                    fontWeight: isDone ? FontWeight.normal : FontWeight.bold,
                    color: isDone ? Pallete.greyColor : Colors.black,
                    decoration: isDone
                        ? TextDecoration.lineThrough
                        : TextDecoration.none,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
