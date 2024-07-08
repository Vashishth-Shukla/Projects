using Microsoft.EntityFrameworkCore.Diagnostics;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NotesApplication.Commands
{
    internal class SearchNoteCommand : ICommand
    {
        private readonly AppDbContext _appDbContext;
        public SearchNoteCommand(AppDbContext appDbContext)
        {
            _appDbContext = appDbContext;
        }

        public void Execute()
        {
            Console.WriteLine("Enter the keyword to find the note:");
            var key = Console.ReadLine();
            
            var notesQuery = _appDbContext.Notes.Where(n => n.Title.Contains(key) || n.Content.Contains(key));

            var notes = notesQuery.ToList();

            if(notes.Any())
            {
                foreach(var note in notes)
                {
                    Console.WriteLine($"Title: {note.Title}");
                    Console.WriteLine($"Content: {note.Content}");
                    Console.WriteLine($"-------------------------------");

                }
            }
            else
            {
                Console.WriteLine("No notes found with the given key");
            }
        }
    }
}
