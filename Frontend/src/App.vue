<template>
  <div class="app-container">
    <!-- Fondo animado con partículas -->
    <div class="background-animation">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
    </div>

    <div class="main-card">
      <div class="card-header">
        <h1 class="app-title">
          <span class="icon-title">👥</span>
          Gestión de Clientes
          <span class="pro-badge">MMJ</span>
        </h1>
        <p class="subtitle">Sistema profesional de administración</p>
      </div>

      <transition name="fade" mode="out-in">
        <!-- PANTALLA DE LOGIN -->
        <div v-if="!token" class="auth-container" key="login">
          <div class="form-card login-card">
            <div class="login-header">
              <div class="login-icon">🔐</div>
              <h3>Bienvenido</h3>
              <p class="login-subtitle">Inicia sesión para continuar</p>
            </div>
            
            <div class="input-group">
              <div class="input-wrapper">
                <span class="input-icon">👤</span>
                <input 
                  v-model="userForm.username" 
                  placeholder="Usuario" 
                  class="modern-input" 
                  @keyup.enter="handleLogin"
                />
              </div>
              
              <div class="input-wrapper">
                <span class="input-icon">🔒</span>
                <input 
                  v-model="userForm.password" 
                  type="password" 
                  placeholder="Contraseña" 
                  class="modern-input"
                  @keyup.enter="handleLogin"
                />
              </div>
            </div>
            
            <button @click="handleLogin" class="btn btn-primary btn-block btn-lg">
              <span class="btn-icon">→</span>
              Entrar al Sistema
            </button>
            
            <div class="login-footer">
              <p>¿Primera vez aquí? Contacta al administrador</p>
            </div>
          </div>
        </div>

        <!-- PANEL PRINCIPAL -->
        <div v-else class="panel-container" key="panel">
          <header class="panel-header">
            <div class="header-left">
              <h3>Panel Administrativo</h3>
              <div class="stats-bar">
                <div class="stat-item">
                  <span class="stat-icon">📊</span>
                  <span class="stat-value">{{ clientes.length }}</span>
                  <span class="stat-label">Clientes</span>
                </div>
                <div class="stat-item">
                  <span class="stat-icon">✅</span>
                  <span class="stat-value">{{ clientesFiltrados.length }}</span>
                  <span class="stat-label">Filtrados</span>
                </div>
              </div>
            </div>
            <button @click="logout" class="btn btn-danger btn-sm">
              <span class="btn-icon">🚪</span>
              Cerrar Sesión
            </button>
          </header>

          <!-- FORMULARIO NUEVO CLIENTE -->
          <section class="form-card new-client-section">
            <div class="section-header">
              <h4 class="section-title">
                <span class="title-icon">➕</span>
                Registrar Nuevo Cliente
              </h4>
              <span class="badge badge-info">Formulario</span>
            </div>
            
            <div class="grid-form">
              <div class="input-wrapper">
                <label class="input-label">Nombre</label>
                <input 
                  v-model="clienteForm.nombre" 
                  placeholder="Ej: Juan" 
                  class="modern-input" 
                />
              </div>
              
              <div class="input-wrapper">
                <label class="input-label">Apellidos</label>
                <input 
                  v-model="clienteForm.apellidos" 
                  placeholder="Ej: García López" 
                  class="modern-input" 
                />
              </div>
              
              <div class="input-wrapper">
                <label class="input-label">Edad</label>
                <input 
                  v-model="clienteForm.edad" 
                  type="number" 
                  placeholder="Ej: 30" 
                  class="modern-input"
                  min="0"
                  max="150"
                />
              </div>
              
              <div class="input-wrapper">
                <label class="input-label">Fecha de Nacimiento</label>
                <input 
                  v-model="clienteForm.fecha_nacimiento" 
                  type="date" 
                  class="modern-input"
                />
              </div>
              
              <div class="input-wrapper">
                <label class="input-label">Teléfono</label>
                <input 
                  v-model="clienteForm.telefono" 
                  placeholder="Ej: 612345678" 
                  class="modern-input" 
                />
              </div>
              
              <div class="input-wrapper full-width">
                <label class="input-label">Dirección</label>
                <input 
                  v-model="clienteForm.direccion" 
                  placeholder="Ej: Calle Principal, 123" 
                  class="modern-input"
                />
              </div>
            </div>
            
            <button @click="crearCliente" class="btn btn-success btn-block btn-lg mt-4">
              <span class="btn-icon">💾</span>
              Guardar Cliente
            </button>
          </section>
          
          <!-- BARRA DE BÚSQUEDA -->
          <div class="search-section">
            <div class="search-wrapper">
              <span class="search-icon">🔍</span>
              <input 
                v-model="filtro" 
                placeholder="Buscar cliente por nombre o apellidos..." 
                class="modern-input search-input" 
              />
              <span v-if="filtro" class="clear-search" @click="filtro = ''">✕</span>
            </div>
          </div>

          <!-- TABLA DE CLIENTES -->
          <div class="table-section">
            <div class="table-header">
              <h4 class="section-title">
                <span class="title-icon">📋</span>
                Lista de Clientes
              </h4>
              <span class="badge badge-primary">{{ clientesFiltrados.length }} registros</span>
            </div>
            
            <div class="table-responsive">
              <table class="modern-table">
                <thead>
                  <tr>
                    <th><span class="th-icon">👤</span> Nombre</th>
                    <th><span class="th-icon">👥</span> Apellidos</th>
                    <th><span class="th-icon">📱</span> Teléfono</th>
                    <th class="text-center"><span class="th-icon">⚙️</span> Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="c in clientesFiltrados" :key="c.id" class="table-row">
                    <td class="fw-bold">
                      <div class="cell-content">
                        <span class="avatar">{{ c.nombre.charAt(0).toUpperCase() }}</span>
                        {{ c.nombre }}
                      </div>
                    </td>
                    <td>{{ c.apellidos }}</td>
                    <td>
                      <span class="phone-badge">{{ c.telefono }}</span>
                    </td>
                    <td class="actions-cell">
                      <button @click="prepararEdicion(c)" class="btn btn-outline-success btn-sm">
                        <span class="btn-icon">✏️</span>
                        Editar
                      </button>
                      <button @click="eliminarCliente(c.id)" class="btn btn-outline-danger btn-sm">
                        <span class="btn-icon">🗑️</span>
                        Borrar
                      </button>
                    </td>
                  </tr>
                  <tr v-if="clientesFiltrados.length === 0">
                    <td colspan="4" class="empty-state">
                      <div class="empty-content">
                        <span class="empty-icon">📭</span>
                        <p class="empty-title">No se encontraron clientes</p>
                        <p class="empty-text">
                          {{ clientes.length === 0 
                            ? 'Comienza agregando tu primer cliente' 
                            : 'Intenta con otro término de búsqueda' 
                          }}
                        </p>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- MODAL DE EDICIÓN -->
    <transition name="modal-fade">
      <div v-if="clienteEnEdicion" class="modal-backdrop" @click.self="clienteEnEdicion = null">
        <div class="modal-content form-card">
          <div class="modal-header">
            <h3 class="modal-title">
              <span class="title-icon">✏️</span>
              Editar Cliente
            </h3>
            <button @click="clienteEnEdicion = null" class="close-btn">✕</button>
          </div>
          
          <div class="flex-form">
            <div class="input-wrapper">
              <label class="input-label">Nombre</label>
              <input 
                v-model="clienteEnEdicion.nombre" 
                placeholder="Nombre" 
                class="modern-input" 
              />
            </div>
            
            <div class="input-wrapper">
              <label class="input-label">Apellidos</label>
              <input 
                v-model="clienteEnEdicion.apellidos" 
                placeholder="Apellidos" 
                class="modern-input" 
              />
            </div>
            
            <div class="input-wrapper">
              <label class="input-label">Teléfono</label>
              <input 
                v-model="clienteEnEdicion.telefono" 
                placeholder="Teléfono" 
                class="modern-input" 
              />
            </div>
            
            <div class="input-wrapper">
              <label class="input-label">Dirección</label>
              <input 
                v-model="clienteEnEdicion.direccion" 
                placeholder="Dirección" 
                class="modern-input" 
              />
            </div>
            
            <div class="modal-actions">
              <button @click="guardarCambios" class="btn btn-success flex-1">
                <span class="btn-icon">✓</span>
                Actualizar
              </button>
              <button @click="clienteEnEdicion = null" class="btn btn-secondary flex-1">
                <span class="btn-icon">✕</span>
                Cancelar
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const API = "http://127.0.0.1:8005"; 
const token = ref(localStorage.getItem('token') || '');
const clientes = ref([]);
const filtro = ref('');
const userForm = ref({ username: '', password: '' });
const clienteForm = ref({ nombre: '', apellidos: '', edad: null, fecha_nacimiento: '', telefono: '', direccion: '' });
const clienteEnEdicion = ref(null);

const clientesFiltrados = computed(() => {
  return clientes.value.filter(c => {
    const nombreCompleto = ${c.nombre} ${c.apellidos}.toLowerCase();
    return nombreCompleto.includes(filtro.value.toLowerCase());
  });
});

const handleLogin = async () => {
  const data = new FormData();
  data.append('username', userForm.value.username);
  data.append('password', userForm.value.password);
  try {
    const res = await axios.post(${API}/login, data);
    token.value = res.data.access_token;
    localStorage.setItem('token', token.value);
    fetchClientes();
  } catch (e) { alert("Error: Revisa usuario o contraseña."); }
};

const fetchClientes = async () => {
  try {
    const res = await axios.get(${API}/clientes/, {
      headers: { Authorization: Bearer ${token.value} }
    });
    clientes.value = res.data;
  } catch (e) { if(e.response?.status === 401) logout(); }
};

const crearCliente = async () => {
  try {
    await axios.post(${API}/clientes/, clienteForm.value, {
      headers: { Authorization: Bearer ${token.value} }
    });
    clienteForm.value = { nombre: '', apellidos: '', edad: null, fecha_nacimiento: '', telefono: '', direccion: '' };
    fetchClientes();
  } catch (e) { 
    alert(e.response?.data?.detail || "Error al crear cliente"); 
  }
};

const eliminarCliente = async (id) => {
  if (!confirm("¿Seguro que quieres eliminar este cliente?")) return;
  try {
    await axios.delete(${API}/clientes/${id}, {
      headers: { Authorization: Bearer ${token.value} }
    });
    fetchClientes();
  } catch (e) { alert("Error al borrar"); }
};

const prepararEdicion = (cliente) => {
  clienteEnEdicion.value = { ...cliente };
};

const guardarCambios = async () => {
  try {
    await axios.put(${API}/clientes/${clienteEnEdicion.value.id}, clienteEnEdicion.value, {
      headers: { Authorization: Bearer ${token.value} }
    });
    clienteEnEdicion.value = null;
    fetchClientes();
  } catch (e) { alert("Error al actualizar"); }
};

const logout = () => { token.value = ''; localStorage.removeItem('token'); };
onMounted(() => { if(token.value) fetchClientes(); });
</script>

<style scoped>
/* --- VARIABLES Y BASE --- */
:root {
  --primary: #42b883;
  --primary-dark: #33a06f;
  --primary-light: #52c893;
  --danger: #ff4444;
  --danger-dark: #cc3333;
  --info: #3498db;
  --dark-bg: #0a0e27;
  --card-bg: #1a1f3a;
  --card-bg-light: #252b47;
  --input-bg: #2d3348;
  --text-light: #f0f0f0;
  --text-muted: #aaa;
  --border-color: #3a4157;
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.2);
  --shadow-md: 0 4px 16px rgba(0,0,0,0.3);
  --shadow-lg: 0 8px 32px rgba(0,0,0,0.4);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* --- FONDO ANIMADO --- */
.background-animation {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
  pointer-events: none;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(66, 184, 131, 0.1) 0%, transparent 70%);
  animation: float 20s infinite ease-in-out;
}

.circle-1 {
  width: 400px;
  height: 400px;
  top: -200px;
  left: -200px;
  animation-delay: 0s;
}

.circle-2 {
  width: 600px;
  height: 600px;
  bottom: -300px;
  right: -300px;
  animation-delay: 7s;
}

.circle-3 {
  width: 300px;
  height: 300px;
  top: 50%;
  right: 10%;
  animation-delay: 14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -30px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
}

/* --- CONTENEDOR PRINCIPAL --- */
.app-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 20px;
  background: linear-gradient(135deg, var(--dark-bg) 0%, #1a1f3a 100%);
  font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: var(--text-light);
  position: relative;
}

.main-card {
  width: 100%;
  max-width: 1200px;
  background: var(--card-bg);
  padding: 40px;
  border-radius: 24px;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-color);
  position: relative;
  z-index: 1;
}

/* --- HEADER DE TARJETA --- */
.card-header {
  text-align: center;
  margin-bottom: 40px;
  padding-bottom: 30px;
  border-bottom: 2px solid var(--border-color);
}

.app-title {
  color: var(--primary);
  font-size: 2.8rem;
  font-weight: 800;
  letter-spacing: -1px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.icon-title {
  font-size: 3rem;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.subtitle {
  color: var(--text-muted);
  font-size: 1.1rem;
  font-weight: 400;
}

.pro-badge {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
  font-size: 0.45em;
  padding: 6px 14px;
  border-radius: 8px;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(66, 184, 131, 0.3);
  transform: translateY(-2px);
}

/* --- TARJETAS Y FORMULARIOS --- */
.form-card {
  background: var(--card-bg-light);
  padding: 30px;
  border-radius: 16px;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-md);
}

.login-card {
  max-width: 450px;
  margin: 0 auto;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-icon {
  font-size: 4rem;
  margin-bottom: 20px;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.login-header h3 {
  font-size: 1.8rem;
  margin-bottom: 8px;
  color: var(--text-light);
}

.login-subtitle {
  color: var(--text-muted);
  font-size: 0.95rem;
}

.login-footer {
  text-align: center;
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid var(--border-color);
}

.login-footer p {
  color: var(--text-muted);
  font-size: 0.9rem;
}

/* --- SECCIONES --- */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--primary);
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.title-icon {
  font-size: 1.5rem;
}

.new-client-section {
  margin-bottom: 30px;
}

/* --- BADGES --- */
.badge {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
}

.badge-primary {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
}

.badge-info {
  background: var(--info);
  color: white;
}

/* --- INPUTS --- */
.input-group {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 25px;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
  position: relative;
}

.input-label {
  color: var(--text-muted);
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.input-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem;
  color: var(--text-muted);
}

.modern-input {
  width: 100%;
  padding: 14px 18px;
  background: var(--input-bg);
  color: var(--text-light);
  border: 2px solid transparent;
  border-radius: 10px;
  transition: all 0.3s ease;
  font-size: 15px;
  font-family: inherit;
}

.input-icon + .modern-input {
  padding-left: 48px;
}

.modern-input:focus {
  outline: none;
  border-color: var(--primary);
  background: #353a52;
  box-shadow: 0 0 0 4px rgba(66, 184, 131, 0.1);
  transform: translateY(-2px);
}

.modern-input::placeholder {
  color: #6b7280;
}

.grid-form {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.full-width {
  grid-column: 1 / -1;
}

.flex-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* --- BÚSQUEDA --- */
.search-section {
  margin: 30px 0;
}

.search-wrapper {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
}

.search-icon {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.3rem;
  z-index: 1;
}

.search-input {
  padding-left: 55px !important;
  padding-right: 45px !important;
  text-align: left;
  box-shadow: var(--shadow-md);
}

.clear-search {
  position: absolute;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: var(--text-muted);
  font-size: 1.2rem;
  font-weight: bold;
  transition: all 0.2s;
  z-index: 1;
}

.clear-search:hover {
  color: var(--danger);
  transform: translateY(-50%) scale(1.2);
}

/* --- BOTONES --- */
.btn {
  padding: 14px 24px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 700;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 15px;
  font-family: inherit;
  box-shadow: var(--shadow-sm);
}

.btn:hover { 
  transform: translateY(-3px); 
  box-shadow: var(--shadow-md);
}

.btn:active { 
  transform: translateY(-1px); 
}

.btn-icon {
  font-size: 1.1em;
}

.btn-block { 
  width: 100%; 
}

.btn-lg {
  padding: 16px 28px;
  font-size: 16px;
}

.btn-sm { 
  padding: 8px 16px; 
  font-size: 13px; 
}

.mt-4 { 
  margin-top: 1.5rem; 
}

.flex-1 { 
  flex: 1; 
}

.btn-primary { 
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
}

.btn-primary:hover { 
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%);
  box-shadow: 0 8px 20px rgba(66, 184, 131, 0.4);
}

.btn-success { 
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
}

.btn-success:hover { 
  box-shadow: 0 8px 20px rgba(16, 185, 129, 0.4);
}

.btn-danger { 
  background: linear-gradient(135deg, var(--danger) 0%, var(--danger-dark) 100%);
  color: white;
}

.btn-danger:hover { 
  box-shadow: 0 8px 20px rgba(255, 68, 68, 0.4);
}

.btn-secondary { 
  background: #64748b;
  color: white;
}

.btn-secondary:hover { 
  background: #475569;
}

.btn-outline-success { 
  background: transparent;
  border: 2px solid var(--primary);
  color: var(--primary);
  box-shadow: none;
}

.btn-outline-success:hover { 
  background: var(--primary);
  color: white;
}

.btn-outline-danger { 
  background: transparent;
  border: 2px solid var(--danger);
  color: var(--danger);
  box-shadow: none;
}

.btn-outline-danger:hover { 
  background: var(--danger);
  color: white;
}

/* --- TABLA --- */
.table-section {
  background: var(--card-bg-light);
  padding: 25px;
  border-radius: 16px;
  border: 1px solid var(--border-color);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-responsive {
  overflow-x: auto;
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
}

.modern-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--card-bg);
}

.modern-table thead th {
  background: linear-gradient(135deg, #2d3348 0%, #252b47 100%);
  padding: 18px;
  font-weight: 700;
  color: var(--primary);
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 1px;
  border-bottom: 2px solid var(--primary);
}

.th-icon {
  margin-right: 8px;
}

.modern-table tbody tr { 
  border-bottom: 1px solid var(--border-color);
  transition: all 0.2s;
}

.modern-table tbody tr:hover { 
  background: var(--card-bg-light);
  transform: translateX(4px);
}

.modern-table tbody td { 
  padding: 18px;
  vertical-align: middle;
}

.cell-content {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.95rem;
}

.phone-badge {
  background: var(--input-bg);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.9rem;
  font-family: 'Courier New', monospace;
  color: var(--primary);
}

.text-center { 
  text-align: center; 
}

.fw-bold { 
  font-weight: 700;
  color: var(--text-light);
}

.actions-cell { 
  display: flex;
  gap: 10px;
  justify-content: center;
  flex-wrap: wrap;
}

.empty-state { 
  padding: 60px 30px;
  text-align: center;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.empty-icon {
  font-size: 4rem;
  opacity: 0.3;
}

.empty-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-light);
}

.empty-text {
  color: var(--text-muted);
  font-size: 0.95rem;
}

/* --- HEADER DEL PANEL --- */
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 30px;
  padding: 25px;
  background: var(--card-bg-light);
  border-radius: 16px;
  border: 1px solid var(--border-color);
}

.header-left {
  flex: 1;
}

.panel-header h3 { 
  margin: 0 0 15px 0;
  font-size: 1.6rem;
  font-weight: 700;
}

.stats-bar {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--input-bg);
  padding: 8px 16px;
  border-radius: 8px;
}

.stat-icon {
  font-size: 1.3rem;
}

.stat-value {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--primary);
}

.stat-label {
  font-size: 0.85rem;
  color: var(--text-muted);
}

/* --- MODAL --- */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.9);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-content {
  width: 90%;
  max-width: 550px;
  border: 2px solid var(--primary);
  animation: slideUp 0.3s ease;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 2px solid var(--border-color);
}

.modal-title { 
  color: var(--primary);
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.close-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 1.8rem;
  cursor: pointer;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s;
}

.close-btn:hover {
  background: var(--danger);
  color: white;
  transform: rotate(90deg);
}

.modal-actions { 
  display: flex;
  gap: 15px;
  margin-top: 25px;
}

/* --- ANIMACIONES --- */
@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(30px) scale(0.95);
  }
  to { 
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.fade-enter-active, 
.fade-leave-active { 
  transition: all 0.4s ease;
}

.fade-enter-from, 
.fade-leave-to { 
  opacity: 0;
  transform: scale(0.95);
}

.modal-fade-enter-active {
  transition: all 0.3s ease;
}

.modal-fade-leave-active {
  transition: all 0.2s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

.modal-fade-enter-from .modal-content {
  transform: translateY(30px) scale(0.95);
}

.modal-fade-leave-to .modal-content {
  transform: translateY(-30px) scale(0.95);
}

/* --- RESPONSIVE --- */
@media (max-width: 768px) {
  .app-title {
    font-size: 2rem;
    flex-direction: column;
    gap: 10px;
  }
  
  .grid-form {
    grid-template-columns: 1fr;
  }
  
  .panel-header {
    flex-direction: column;
    gap: 20px;
  }
  
  .stats-bar {
    width: 100%;
  }
  
  .stat-item {
    flex: 1;
    justify-content: center;
  }
  
  .actions-cell {
    flex-direction: column;
  }
  
  .modern-table {
    font-size: 13px;
  }
  
  .modern-table thead th,
  .modern-table tbody td {
    padding: 12px;
  }
  
  .main-card {
    padding: 20px;
  }
}

@media (max-width: 480px) {
  .app-title {
    font-size: 1.6rem;
  }
  
  .icon-title {
    font-size: 2rem;
  }
}
</style>