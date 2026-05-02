import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authService } from '../services/auth.service';
import { toast } from 'sonner';
import type { LoginCredentials, RegisterDocenteData, Usuario } from '../types/auth.types';

interface AuthState {
  user: Usuario | null;
  token: string | null;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<boolean>;
  registerDocente: (data: RegisterDocenteData) => Promise<boolean>;
  logout: () => Promise<void>;
  loadUser: () => Promise<void>;
  clearAuth: () => void;
}

const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: localStorage.getItem('access_token'),
      isLoading: false,

      login: async (credentials) => {
        set({ isLoading: true });
        try {
          const response = await authService.login(credentials);
          localStorage.setItem('access_token', response.access_token);
          set({ token: response.access_token });
          
          // Cargar datos del usuario
          const user = await authService.getCurrentUser();
          set({ user });
          localStorage.setItem('user', JSON.stringify(user));
          
          toast.success(`Bienvenido, ${user.nombre} ${user.apellido}`);
          return true;
        } catch (error: any) {
          console.log(error);
          const message = error.response?.data?.detail || 'Error al iniciar sesión';
          toast.error(message);
          return false;
        } finally {
          set({ isLoading: false });
        }
      },

      registerDocente: async (data) => {
        set({ isLoading: true });
        try {
          const newDocente = await authService.registerDocente(data);
          toast.success(`Docente ${newDocente.nombre} ${newDocente.apellido} registrado exitosamente`);
          return true;
        } catch (error: any) {
          const message = error.response?.data?.detail || 'Error al registrar docente';
          toast.error(message);
          return false;
        } finally {
          set({ isLoading: false });
        }
      },

      logout: async () => {
        set({ isLoading: true });
        try {
          await authService.logout();
          toast.info('Sesión cerrada exitosamente');
        } catch (error) {
          console.error('Error en logout:', error);
        } finally {
          get().clearAuth();
          set({ isLoading: false });
        }
      },

      loadUser: async () => {
        const token = localStorage.getItem('access_token');
        if (!token) return;
        
        set({ isLoading: true });
        try {
          const user = await authService.getCurrentUser();
          set({ user, token });
          localStorage.setItem('user', JSON.stringify(user));
        } catch (error) {
          console.error('Error loading user:', error);
          get().clearAuth();
        } finally {
          set({ isLoading: false });
        }
      },

      clearAuth: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        set({ user: null, token: null });
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user, token: state.token }),
    }
  )
);

export default useAuthStore;
