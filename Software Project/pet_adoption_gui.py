import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import PhotoImage
from process_data import add_pet, remove_pet, update_pet, fetch_pets
from process_data import export_pets_to_csv
from process_data import PET_FILE
from process_data import import_pets_from_csv
from datetime import datetime


class PetAdoptionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pet Adoption Management")
        self.root.geometry("1800x750")
        self.root.configure(bg="#f4f4f4")

        # Main Layout: Input Frame and Table Frame
        self.input_frame = tk.Frame(root, bg="#e8f8ff", padx=10, pady=10)
        self.input_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        self.table_frame = tk.Frame(root, bg="#ffffff", padx=10, pady=10)
        self.table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_input_section()
        self.create_table_section()

    def create_input_section(self):
        tk.Label(self.input_frame, text="Pet ID", bg="#e8f8ff").grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(self.input_frame, text="Name", bg="#e8f8ff").grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(self.input_frame, text="Species", bg="#e8f8ff").grid(row=2, column=0, sticky="w", pady=5)
        tk.Label(self.input_frame, text="Age (Months)", bg="#e8f8ff").grid(row=3, column=0, sticky="w", pady=5)
        tk.Label(self.input_frame, text="Gender", bg="#e8f8ff").grid(row=4, column=0, sticky="w", pady=5)
        tk.Label(self.input_frame, text="Weight (kg)", bg="#e8f8ff").grid(row=5, column=0, sticky="w", pady=5)
        tk.Label(self.input_frame, text="Description", bg="#e8f8ff").grid(row=6, column=0, sticky="w", pady=5)
        
        self.entries = {}
        for idx, field in enumerate([
            "pet_id", "name", "species", "age", "gender", "weight", "description"
        ]):
            self.entries[field] = tk.Entry(self.input_frame, width=30)
            self.entries[field].grid(row=idx, column=1, pady=5)

        self.action_buttons = tk.Frame(self.input_frame, bg="#e8f8ff", pady=10)
        self.action_buttons.grid(row=7, column=0, columnspan=2)
        

        tk.Button(self.action_buttons, text="Add Pet", command=self.add_pet, bg="#4caf50", fg="#ffffff", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(self.action_buttons, text="Update Pet", command=self.update_pet, bg="#ffa500", fg="#ffffff", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(self.action_buttons, text="Delete Pet", command=self.delete_pet, bg="#f44336", fg="#ffffff", width=15).pack(side=tk.LEFT, padx=5)
       
        self.action_buttons = tk.Frame(self.input_frame, bg="#e8f8ff", pady=10)
        self.action_buttons.grid(row=8, column=0, columnspan=2)
        
        tk.Button(self.action_buttons, text="Export to CSV", command=self.export_to_csv, bg="#2196f3", fg="#ffffff", width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(self.action_buttons, text="Import CSV", command=self.import_csv, bg="#673ab7", fg="#ffffff", width=15).pack(side=tk.LEFT, padx=5)

        self.photo_frame = tk.Frame(self.input_frame, bg="#e8f8ff", pady=10)
        self.photo_frame.grid(row=9, column=0, columnspan=2)

        # Load and display the image
        try:
            image_path = "pic.png"  # Replace with the path to your image
            self.pet_image = PhotoImage(file=image_path)
            
           
            self.pet_image = self.pet_image.subsample(3, 3) 

            self.image_label = tk.Label(self.photo_frame, image=self.pet_image, bg="#e8f8ff")
            self.image_label.pack()
        except Exception:
            pass  


    def create_table_section(self):
        tk.Label(self.table_frame, text="Pets List", bg="#ffffff", font=("Arial", 16, "bold")).pack(anchor="w", pady=5)

        # Define Treeview with columns
        self.tree = ttk.Treeview(self.table_frame, columns=(
            "ID", "Name", "Species", "Age", "Gender", "Weight", "Description"
        ), show="headings", height=20)

        # Configure the table headings and columns
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            if col == "Description":
                self.tree.column(col, width=300, anchor="w", stretch=tk.YES)  # Make Description column wider
            else:
                self.tree.column(col, width=100, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Define alternating row colors
        self.tree.tag_configure("oddrow", background="#e8f4f8")
        self.tree.tag_configure("evenrow", background="#f9fbfd")

        self.refresh_table()

    def add_pet(self):
        data = {key: entry.get() for key, entry in self.entries.items()}

        if not all(data.values()):
            messagebox.showerror("Error", "Please fill in all fields to add a new pet.")
            return

        try:
            add_pet(data["pet_id"], data["name"], data["species"], data["age"], data["gender"], data["weight"], data["description"])
            self.refresh_table()
            self.clear_inputs()
            messagebox.showinfo("Success", "Pet added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_pet(self):
        data = {key: entry.get() for key, entry in self.entries.items()}
        pet_id = data.get("pet_id")

        if not pet_id:
            messagebox.showerror("Error", "Pet ID is required to update.")
            return

        try:
            update_pet(pet_id, data["name"], data["species"], data["age"], data["gender"], data["weight"], data["description"])
            self.refresh_table()
            self.clear_inputs()
            messagebox.showinfo("Success", "Pet updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_pet(self):
        pet_id = self.entries["pet_id"].get()
        if not pet_id:
            messagebox.showerror("Error", "Pet ID is required to delete a pet.")
            return

        try:
            remove_pet(pet_id)
            self.refresh_table()
            self.clear_inputs()
            messagebox.showinfo("Success", "Pet removed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_table(self, pets=None):
    # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

    # Fetch pets if none provided
        pets = pets or fetch_pets()
        for index, pet in enumerate(pets):
            tag = "oddrow" if index % 2 == 0 else "evenrow"
            self.tree.insert("", "end", values=pet, tags=(tag,))

    def clear_inputs(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)


    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=f"pets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                export_pets_to_csv(file_path)
                messagebox.showinfo("Success", "Data exported to CSV successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))




    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            choice = messagebox.askyesnocancel(
                "Import Options",
                "Do you want to overwrite existing data? (Yes to overwrite, No to merge, Cancel to abort)"
            )

            if choice is None:  # Cancel
                return
            try:
                pets = import_pets_from_csv(file_path, overwrite=choice)
                self.refresh_table(pets if choice else fetch_pets())
                messagebox.showinfo("Success", "Data imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = PetAdoptionGUI(root)
    root.mainloop()

#FINAL 