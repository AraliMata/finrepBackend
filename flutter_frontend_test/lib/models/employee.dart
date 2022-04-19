class Employee {
  final String eemail;
  final String ename;

  Employee({required this.eemail, required this.ename});

  factory Employee.fromJson(Map<String, dynamic> json) {
    return Employee(
      ename: json['ename'],
      eemail: json['eemail'],
    );
  }

  Map<String, dynamic> toJson() => {
        'ename': ename,
        'eemail': eemail,
      };
}
