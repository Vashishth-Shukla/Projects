using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using TodoList.Models;

namespace TodoList.DataServices
{
    public class TaskDataService
    {
        private readonly string _filePath;
        private readonly string folderName = "TodoList";
        private readonly string fileName = "tasks.json";

        public TaskDataService()
        {
            // the path appdatat
            string appDataPath = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            // golder of the app in roaming
            string appFolder = Path.Combine(appDataPath, folderName);
            // data folder inside app
            string dataFolder = Path.Combine(appFolder, "data");

            // if the folder not there create the folder 
            if (!Directory.Exists(dataFolder))
            {
                Directory.CreateDirectory(dataFolder);
            }
            // define the path to the json file
            _filePath = Path.Combine(dataFolder, fileName);

            // initialize json file
            InitializerFile();
        }

        private void InitializerFile()
        {
            if (!File.Exists(_filePath))
            {
                File.WriteAllText(_filePath, JsonConvert.SerializeObject(new List<Task>()));
            }
            // debug
            Process.Start(Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), folderName));
        }

        public List<Task> LoadTasks()
        {
            // read the JSON file
            string fileContent = File.ReadAllText(_filePath);
            return JsonConvert.DeserializeObject<List<Task>>(fileContent);
        }

        public void SaveTasks(List<Task> tasks)
        {
            string json = JsonConvert.SerializeObject(tasks, Formatting.Indented);
            File.WriteAllText(_filePath, json);
        }

        public void AddTask(Task newTask)
        {
            newTask.Id = GenerateNewTaskId();
            var tasks = LoadTasks();
            tasks.Add(newTask);
            SaveTasks(tasks);
        }

        public int GenerateNewTaskId()
        {
            var tasks = LoadTasks();

            if (!tasks.Any()) { return 1; }

            int maxId = tasks.Max(task => (int)task.Id);
            return maxId + 1;
        }

        public void UpdateTask(Task updateTask)
        {
            var tasks = LoadTasks();
            var taskIndex = tasks.FindIndex(t => t.Id == updateTask.Id); // match the ID
            if (taskIndex != -1) // validate the ID
            {
                tasks[taskIndex] = updateTask; // JSON data update
                SaveTasks(tasks);
            }
        }

        public void DeleteTask(int taskId)
        {
            var tasks = LoadTasks();
            tasks.RemoveAll(task => task.Id == taskId);
            SaveTasks(tasks);
        }
    }
}
