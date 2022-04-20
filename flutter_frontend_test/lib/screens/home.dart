import 'package:flutter/material.dart';
import 'package:flutter_frontend_test/models/cuentas.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:developer' as developer;

import '../env.sample.dart';
import '../models/employee.dart';
import '../models/cuentas.dart';

class Home extends StatefulWidget {
  const Home({Key? key}) : super(key: key);
  @override
  MyAppState2 createState() => MyAppState2();
}

class HomeState extends State<Home> {
  late Future<List<Employee>> employees = getEmployeeList();
  final employeeListKey = GlobalKey<HomeState>();
/* 
  @override
  void initState() {
    super.initState();
    employees = getEmployeeList();
  }
 */

  Future<List<Employee>> getEmployeeList() async {
    final response =
        await http.get(Uri.parse("${Env.URL_PREFIX}/employeedetails"));
    final items = json.decode(response.body).cast<Map<String, dynamic>>();
    List<Employee> employees = items.map<Employee>((json) {
      return Employee.fromJson(json);
    }).toList();

    return employees;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: employeeListKey,
      appBar: AppBar(
        title: Text('Employee List'),
      ),
      body: Center(
        child: FutureBuilder<List<Employee>>(
          future: employees,
          builder: (BuildContext context, AsyncSnapshot snapshot) {
            // By default, show a loading spinner.
            if (!snapshot.hasData) return CircularProgressIndicator();
            // Render employee lists
            return ListView.builder(
              itemCount: snapshot.data.length,
              itemBuilder: (BuildContext context, int index) {
                var data = snapshot.data[index];
                return Card(
                  child: ListTile(
                    leading: Icon(Icons.person),
                    title: Text(
                      data.ename,
                      style: TextStyle(fontSize: 20),
                    ),
                  ),
                );
              },
            );
          },
        ),
      ),
    );
  }
}

Future<Employee> registerEmployee(String name, String email) async {
  final response = await http.post(
    Uri.parse("${Env.URL_PREFIX}/employeedetails"),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{'ename': name, 'eemail': email}),
  );
  if (response.statusCode == 201) {
    // If the server did return a 201 CREATED response,
    // then parse the JSON.
    return Employee.fromJson(jsonDecode(response.body));
  } else {
    // If the server did not return a 201 CREATED response,
    // then throw an exception.
    throw Exception('Failed to register employee.');
  }
}

Future<Cuentas> registrarCuenta(
    String idEmpresa, String codigo, String nombre) async {
  final response = await http.post(
    Uri.parse("${Env.URL_PREFIX}/cuentas"),
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, String>{
      'idEmpresa': idEmpresa,
      'codigo': codigo,
      'nombre': nombre
    }),
  );
  if (response.statusCode == 201) {
    // If the server did return a 201 CREATED response,
    // then parse the JSON.
    return Cuentas.fromJson(jsonDecode(response.body));
  } else {
    // If the server did not return a 201 CREATED response,
    // then throw an exception.
    throw Exception('Failed to register account.');
  }
}

// class Register extends StatefulWidget {
//   const Register({Key? key}) : super(key: key);
//   @override
//   MyAppState createState() => MyAppState();
// }

class MyAppState extends State<Home> {
  final TextEditingController _controller = TextEditingController();
  final TextEditingController _controller2 = TextEditingController();
  // final TextEditingController _controller3 = TextEditingController();
  Future<Employee>? _futureEmployee;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Create Data Example',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Create Data Example'),
        ),
        body: Container(
          alignment: Alignment.center,
          padding: const EdgeInsets.all(8.0),
          child:
              (_futureEmployee == null) ? buildColumn() : buildFutureBuilder(),
        ),
      ),
    );
  }

  Column buildColumn() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        TextField(
          controller: _controller,
          decoration: const InputDecoration(hintText: 'Enter name'),
        ),
        TextField(
          controller: _controller2,
          decoration: const InputDecoration(hintText: 'Enter email'),
        ),
        // TextField(
        //   controller: _controller3,
        //   decoration: const InputDecoration(hintText: 'Enter nombre'),
        // ),
        ElevatedButton(
          onPressed: () {
            setState(() {
              _futureEmployee =
                  registerEmployee(_controller.text, _controller2.text);
            });
          },
          child: const Text('Create Data'),
        ),
      ],
    );
  }

  FutureBuilder<Employee> buildFutureBuilder() {
    return FutureBuilder<Employee>(
      future: _futureEmployee,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          return Text(snapshot.data!.ename);
        } else if (snapshot.hasError) {
          return Text('${snapshot.error}');
        }

        return const CircularProgressIndicator();
      },
    );
  }
}

class MyAppState2 extends State<Home> {
  final TextEditingController _controller = TextEditingController();
  final TextEditingController _controller2 = TextEditingController();
  final TextEditingController _controller3 = TextEditingController();
  Future<Cuentas>? _futureAccount;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Create Data Example',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Create Data Example'),
        ),
        body: Container(
          alignment: Alignment.center,
          padding: const EdgeInsets.all(8.0),
          child:
              (_futureAccount == null) ? buildColumn() : buildFutureBuilder(),
        ),
      ),
    );
  }

  Column buildColumn() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        TextField(
          controller: _controller,
          decoration: const InputDecoration(hintText: 'Enter empresa'),
        ),
        TextField(
          controller: _controller2,
          decoration: const InputDecoration(hintText: 'Enter codigo'),
        ),
        TextField(
          controller: _controller3,
          decoration: const InputDecoration(hintText: 'Enter nombre'),
        ),
        ElevatedButton(
          onPressed: () {
            setState(() {
              _futureAccount = registrarCuenta(
                  _controller.text, _controller2.text, _controller3.text);
            });
          },
          child: const Text('Create Data'),
        ),
      ],
    );
  }

  FutureBuilder<Cuentas> buildFutureBuilder() {
    return FutureBuilder<Cuentas>(
      future: _futureAccount,
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          return Text(snapshot.data!.nombre);
        } else if (snapshot.hasError) {
          return Text('${snapshot.error}');
        }

        return const CircularProgressIndicator();
      },
    );
  }
}
