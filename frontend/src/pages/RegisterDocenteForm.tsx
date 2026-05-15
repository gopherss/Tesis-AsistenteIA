import { useEffect, useState } from 'react';

import {
  Button,
  DashboardLayout,
  Input
} from '../components';

import { toast } from 'sonner';

import {
  authService
} from '../services/auth.service';

import {
  useAuthStore
} from '../store';

import type {
  RegisterDocenteData,
  Usuario,
  UpdateDocenteData
} from '../types/auth.types';

import {
  validarFormularioRegistro,
  validarFormularioEdicion,
  validarNombre,
  validarEmail,
  validarPassword,
} from '../utils';

import type { ErroresRegistro, ErroresEdicion } from '../utils';


const RegisterDocenteForm = () => {

  const {
    registerDocente,
    isLoading
  } = useAuthStore();

  const [docentes, setDocentes] = useState<Usuario[]>([]);

  const [page, setPage] = useState(1);

  const [total, setTotal] = useState(0);

  const limit = 5;

  const [editModal, setEditModal] = useState(false);
  const [deleteModal, setDeleteModal] = useState(false);

  const [docenteToDelete, setDocenteToDelete] =
    useState<Usuario | null>(null);

  const [selectedDocente, setSelectedDocente] =
    useState<Usuario | null>(null);

  const [editData, setEditData] =
    useState<UpdateDocenteData>({
      nombre: '',
      apellido: '',
      email: ''
    });

  const [errores, setErrores] = useState<ErroresRegistro>({});
  const [editErrores, setEditErrores] = useState<ErroresEdicion>({});

  const [formData, setFormData] =
    useState<RegisterDocenteData>({
      email: '',
      password: '',
      nombre: '',
      apellido: '',
      rol: 'DOCENTE',
    });

  const loadDocentes = async () => {

    try {

      const response =
        await authService.getDocentes(page, limit);

      setDocentes(response.data);
      setTotal(response.total);

    } catch {
      toast.error('Error cargando docentes');
    }
  };

  useEffect(() => {
    loadDocentes();
  }, [page]);

  const validarYEnviar = async () => {
    const errs = validarFormularioRegistro(formData);
    setErrores(errs);

    if (Object.keys(errs).length > 0) {
      toast.error(Object.values(errs)[0]);
      return;
    }

    const success = await registerDocente(formData);

    if (success) {
      setFormData({
        email: '',
        password: '',
        nombre: '',
        apellido: '',
        rol: 'DOCENTE'
      });
      setErrores({});
      loadDocentes();
    }
  };

  const handleSubmit = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();
    await validarYEnviar();
  };

  const openDeleteModal = (docente: Usuario) => {
    setDocenteToDelete(docente);
    setDeleteModal(true);
  };

  const handleDelete = async () => {

    if (!docenteToDelete?.id) return;

    try {

      await authService.deleteDocente(
        docenteToDelete.id
      );

      toast.success('Docente eliminado');

      setDeleteModal(false);

      loadDocentes();

    } catch {

      toast.error('Error eliminando');
    }
  };


  const openEditModal = (
    docente: Usuario
  ) => {

    setSelectedDocente(docente);

    setEditData({
      nombre: docente.nombre,
      apellido: docente.apellido,
      email: docente.email
    });

    setEditErrores({});
    setEditModal(true);
  };

  const handleUpdate = async () => {
    if (!selectedDocente?.id) return;

    const errs = validarFormularioEdicion(editData);
    setEditErrores(errs);

    if (Object.keys(errs).length > 0) {
      toast.error(Object.values(errs)[0]);
      return;
    }

    try {

      await authService.updateDocente(
        selectedDocente.id,
        editData
      );

      toast.success('Docente actualizado');

      setEditModal(false);

      loadDocentes();

    } catch {
      toast.error('Error actualizando');
    }
  };

  const totalPages = Math.ceil(total / limit);

  return (
    <DashboardLayout>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* FORM */}

        <div className="bg-white p-6 rounded-lg shadow">

          <h2 className="text-xl font-bold mb-4">
            Registrar Docente
          </h2>

          <form
            onSubmit={handleSubmit}
            className="space-y-4"
          >

            <Input
              label="Nombre"
              value={formData.nombre}
              onChange={(e) => {
                setFormData({ ...formData, nombre: e.target.value });
                setErrores((prev) => ({ ...prev, nombre: validarNombre(e.target.value, "Nombre") || undefined }));
              }}
              error={errores.nombre}
            />

            <Input
              label="Apellido"
              value={formData.apellido}
              onChange={(e) => {
                setFormData({ ...formData, apellido: e.target.value });
                setErrores((prev) => ({ ...prev, apellido: validarNombre(e.target.value, "Apellido") || undefined }));
              }}
              error={errores.apellido}
            />

            <Input
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => {
                setFormData({ ...formData, email: e.target.value });
                setErrores((prev) => ({ ...prev, email: validarEmail(e.target.value) || undefined }));
              }}
              error={errores.email}
            />

            <Input
              label="Contraseña"
              type="password"
              value={formData.password}
              onChange={(e) => {
                setFormData({ ...formData, password: e.target.value });
                setErrores((prev) => ({ ...prev, password: validarPassword(e.target.value) || undefined }));
              }}
              error={errores.password}
            />

            <Button
              type="submit"
              label={
                isLoading
                  ? 'Registrando...'
                  : 'Registrar'
              }
              color="primary"
              full
            />

          </form>
        </div>

        {/* TABLA */}

        <div className="lg:col-span-2 bg-white p-6 rounded-lg shadow">

          <h2 className="text-xl font-bold mb-4">
            Lista de Docentes
          </h2>

          <div className="overflow-x-auto">

            <table className="w-full border">

              <thead className="bg-gray-100">

                <tr>
                  <th className="p-3 border">Nombre</th>
                  <th className="p-3 border">Apellido</th>
                  <th className="p-3 border">Email</th>
                  <th className="p-3 border">Acciones</th>
                </tr>

              </thead>

              <tbody>

                {docentes.map((docente) => (

                  <tr key={docente.id}>

                    <td className="p-3 border">
                      {docente.nombre}
                    </td>

                    <td className="p-3 border">
                      {docente.apellido}
                    </td>

                    <td className="p-3 border">
                      {docente.email}
                    </td>

                    <td className="p-3 border">

                      <div className="flex gap-2">

                        <button
                          onClick={() =>
                            openEditModal(docente)
                          }
                          className="bg-blue-500 text-white px-3 py-1 rounded"
                        >
                          Editar
                        </button>

                        <button
                          onClick={() =>
                            openDeleteModal(docente)
                          }
                          className="bg-red-500 text-white px-3 py-1 rounded"
                        >
                          Eliminar
                        </button>
                      </div>

                    </td>

                  </tr>
                ))}

              </tbody>

            </table>

          </div>

          {/* PAGINACIÓN */}

          <div className="flex justify-center gap-3 mt-5">

            <button
              disabled={page === 1}
              onClick={() => setPage(page - 1)}
              className="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
            >
              Anterior
            </button>

            <span className="flex items-center">
              Página {page} de {totalPages}
            </span>

            <button
              disabled={page === totalPages}
              onClick={() => setPage(page + 1)}
              className="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
            >
              Siguiente
            </button>

          </div>

        </div>

      </div>

      {/* MODAL EDITAR */}

      {editModal && (

        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">

          <div className="bg-white p-6 rounded-lg w-full max-w-md">

            <h2 className="text-xl font-bold mb-4">
              Editar Docente
            </h2>

            <div className="space-y-4">

              <Input
                label="Nombre"
                value={editData.nombre}
                onChange={(e) => {
                  setEditData({ ...editData, nombre: e.target.value });
                  setEditErrores((prev) => ({ ...prev, nombre: validarNombre(e.target.value, "Nombre") || undefined }));
                }}
                error={editErrores.nombre}
              />

              <Input
                label="Apellido"
                value={editData.apellido}
                onChange={(e) => {
                  setEditData({ ...editData, apellido: e.target.value });
                  setEditErrores((prev) => ({ ...prev, apellido: validarNombre(e.target.value, "Apellido") || undefined }));
                }}
                error={editErrores.apellido}
              />

              <Input
                label="Email"
                value={editData.email}
                onChange={(e) => {
                  setEditData({ ...editData, email: e.target.value });
                  setEditErrores((prev) => ({ ...prev, email: validarEmail(e.target.value) || undefined }));
                }}
                error={editErrores.email}
              />

              <div className="flex justify-end gap-3">

                <button
                  onClick={() =>
                    setEditModal(false)
                  }
                  className="px-4 py-2 bg-gray-300 rounded"
                >
                  Cancelar
                </button>

                <button
                  onClick={handleUpdate}
                  className="px-4 py-2 bg-blue-500 text-white rounded"
                >
                  Guardar
                </button>

              </div>

            </div>

          </div>

        </div>

      )}

      {/* MODAL DELETE */}

      {deleteModal && docenteToDelete && (

        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">

          <div className="bg-white p-6 rounded-lg w-full max-w-md">

            <h2 className="text-xl font-bold mb-4 text-red-600">
              Eliminar Docente
            </h2>

            <p className="text-gray-700 mb-6">

              ¿Seguro que deseas eliminar a:

              <span className="font-semibold">
                {" "}
                {docenteToDelete.nombre}{" "}
                {docenteToDelete.apellido}
              </span>?

            </p>

            <div className="flex justify-end gap-3">

              <button
                onClick={() =>
                  setDeleteModal(false)
                }
                className="px-4 py-2 bg-gray-300 rounded"
              >
                Cancelar
              </button>

              <button
                onClick={handleDelete}
                className="px-4 py-2 bg-red-500 text-white rounded"
              >
                Eliminar
              </button>

            </div>

          </div>

        </div>

      )}

    </DashboardLayout>
  );
};

export default RegisterDocenteForm;
