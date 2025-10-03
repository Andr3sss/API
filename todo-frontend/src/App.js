import React, { useState, useEffect } from 'react';

import { Check, X, Plus } from 'lucide-react'; 


const API_BASE_URL = "http://3.142.230.102:8000"; 

// Componente principal de la aplicación
const App = () => {
  const [tasks, setTasks] = useState([]);
  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Funcionalidad 1: Listar todas las tareas (GET /tasks)
  const fetchTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      // Intenta conectar a la API
      const response = await fetch(`${API_BASE_URL}/tasks/`);
      if (!response.ok) {
        throw new Error("Error al obtener las tareas.");
      }
      const data = await response.json();
      setTasks(data.reverse()); 
    } catch (e) {
      setError(e.message || "No se pudo conectar al backend de FastAPI. Verifica la URL y CORS.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);


  const createTask = async (e) => {
    e.preventDefault();
    if (!newTaskTitle.trim()) return;

    try {
      const response = await fetch(`${API_BASE_URL}/tasks/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            title: newTaskTitle.trim(), 
            description: "", 
            completed: false 
        }),
      });

      if (!response.ok) {
        throw new Error("Fallo al crear la tarea.");
      }
      setNewTaskTitle("");
      fetchTasks(); 
    } catch (e) {
      setError(e.message || "Error de red al crear.");
    }
  };



  const toggleTaskCompleted = async (task) => {
    const updatedTask = { ...task, completed: !task.completed };
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${task.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title: updatedTask.title,
          description: updatedTask.description,
          completed: updatedTask.completed
        }),
      });

      if (!response.ok) {
        throw new Error("Fallo al actualizar la tarea.");
      }
      setTasks(tasks.map(t => t.id === task.id ? updatedTask : t));

    } catch (e) {
      setError(e.message || "Error de red al actualizar.");
    }
  };

  const deleteTask = async (id) => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
        method: 'DELETE',
      });

      if (response.status !== 204) {
        throw new Error("Fallo al eliminar la tarea.");
      }
      setTasks(tasks.filter(t => t.id !== id));
    } catch (e) {
      setError(e.message || "Error de red al eliminar.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center p-4 font-sans">
      <div className="w-full max-w-lg bg-white shadow-xl rounded-xl p-6 md:p-8 mt-10">
        <h1 className="text-3xl font-extrabold text-gray-800 mb-6 text-center">
          ToDo App (RDS + FastAPI + React)
        </h1>
        
        <form onSubmit={createTask} className="flex gap-3 mb-6">
          <input
            type="text"
            placeholder="Título de la nueva tarea..."
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            className="flex-grow p-3 border border-gray-300 rounded-lg focus:ring-blue-600 focus:border-blue-600 transition duration-150"
            disabled={loading}
          />
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-semibold shadow-md flex items-center justify-center transition duration-150 disabled:bg-gray-400"
            disabled={loading || !newTaskTitle.trim()}
          >
            <Plus size={20} />
          </button>
        </form>


        {error && (
          <div className="p-3 mb-4 text-sm text-red-700 bg-red-100 rounded-lg" role="alert">
            <p>Error de Conexión. Revisa la IP pública y la configuración CORS de tu FastAPI.</p>
            <p className='font-mono text-xs mt-1'>Conectando a: {API_BASE_URL}</p>
          </div>
        )}
        {loading && !tasks.length && (
             <div className="p-4 text-center text-blue-600">Cargando tareas...</div>
        )}

        {/* Lista de Tareas (Listar) */}
        <div className="space-y-3">
          {tasks.length === 0 && !loading && !error && (
            <p className="text-center text-gray-500 py-4">No hay tareas pendientes. ¡Empieza a crear!</p>
          )}

          {tasks.map((task) => (
            <div
              key={task.id}
              className={`flex items-center p-4 rounded-lg shadow-sm transition duration-200 
                ${task.completed ? 'bg-green-50 border-l-4 border-green-500' : 'bg-gray-50 hover:bg-gray-100'}`
              }
            >
              
              {/* Botón de Completado (Marcar) */}
              <button
                onClick={() => toggleTaskCompleted(task)}
                className={`w-6 h-6 flex items-center justify-center rounded-full border-2 transition duration-150 mr-3 
                  ${task.completed 
                    ? 'bg-green-500 border-green-500 text-white' 
                    : 'border-gray-300 text-transparent hover:border-blue-500 hover:text-blue-500'}`
                }
                title={task.completed ? "Marcar como pendiente" : "Marcar como completada"}
              >
                {task.completed && <Check size={16} />}
              </button>

              {/* Título de la Tarea */}
              <span className={`flex-grow text-gray-800 ${task.completed ? 'line-through text-gray-400' : ''}`}>
                {task.title}
              </span>

              {/* Botón de Eliminar */}
              <button
                onClick={() => deleteTask(task.id)}
                className="ml-3 text-gray-400 hover:text-red-600 transition duration-150 p-1 rounded-full hover:bg-red-100"
                title="Eliminar tarea"
              >
                <X size={18} />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default App;
