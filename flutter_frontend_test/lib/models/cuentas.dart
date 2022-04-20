class Cuentas {
  final int idEmpresa;
  final String codigo;
  final String nombre;

  Cuentas(
      {required this.idEmpresa, required this.codigo, required this.nombre});

  factory Cuentas.fromJson(Map<String, dynamic> json) {
    return Cuentas(
      idEmpresa: json['idEmpresa'],
      codigo: json['codigo'],
      nombre: json['nombre'],
    );
  }

  Map<String, dynamic> toJson() => {
        'idEmpresa': idEmpresa,
        'codigo': codigo,
        'nombre': nombre,
      };
}
