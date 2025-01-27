import 'package:capstone_sams/constants/theme/pallete.dart';
import 'package:capstone_sams/constants/theme/sizing.dart';
import 'package:capstone_sams/providers/MedicalNotesProvider.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'TodoWidget.dart';

class TodoListWidget extends StatelessWidget {
  const TodoListWidget({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = Provider.of<TodosProvider>(context);
    final todos = provider.todos;

    return todos.isEmpty
        ? const Center(
            child: Text(
              'No notes.',
              style: TextStyle(
                  fontSize: Sizing.header6,
                  fontWeight: FontWeight.bold,
                  color: Pallete.greyColor),
            ),
          )
        : ListView.separated(
            physics: const BouncingScrollPhysics(),
            padding: const EdgeInsets.all(16),
            itemBuilder: (context, index) {
              final todo = todos[index];
              return TodoWidget(todo: todo);
            },
            itemCount: todos.length,
            separatorBuilder: (BuildContext context, int index) {
              return Container(
                height: Sizing.formSpacing / 2,
              );
            },
          );
  }
}
