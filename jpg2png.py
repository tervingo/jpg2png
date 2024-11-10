import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
from PIL import Image
import os

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JPG to PNG Converter")
        self.root.geometry("500x300")  # Made slightly taller for the new button
        
        # Create main frame
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(expand=True, fill='both')
        
        # Default color to make transparent (white)
        self.transparency_color = (255, 255, 255)
        self.tolerance = 30  # Color matching tolerance
        
        # Create and pack widgets
        self.create_widgets()
        
    def create_widgets(self):
        # Title label
        title_label = tk.Label(
            self.main_frame, 
            text="JPG to PNG Converter",
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Color selection button
        self.color_button = tk.Button(
            self.main_frame,
            text="Select Color to Make Transparent",
            command=self.select_color,
            width=25,
            height=1
        )
        self.color_button.pack(pady=5)
        
        # File selection button
        self.select_button = tk.Button(
            self.main_frame,
            text="Select JPG File",
            command=self.select_file,
            width=20,
            height=2
        )
        self.select_button.pack(pady=10)
        
        # Selected file label
        self.file_label = tk.Label(
            self.main_frame,
            text="No file selected",
            wraplength=400
        )
        self.file_label.pack(pady=10)
        
        # Quit button
        self.quit_button = tk.Button(
            self.main_frame,
            text="Quit",
            command=self.quit_app,
            width=20,
            height=1,
            bg='#ff9999'  # Light red background
        )
        self.quit_button.pack(pady=10)
        
    def quit_app(self):
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.root.quit()
            self.root.destroy()
    
    def select_color(self):
        color = colorchooser.askcolor(title="Select color to make transparent")
        if color[0]:  # color[0] contains RGB values
            self.transparency_color = tuple(map(int, color[0]))
            messagebox.showinfo(
                "Color Selected",
                f"Selected color RGB: {self.transparency_color}"
            )
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JPEG files", "*.jpg;*.jpeg")]
        )
        
        if file_path:
            self.file_label.config(text=f"Selected: {file_path}")
            self.convert_image(file_path)
    
    def is_similar_color(self, color1, color2, tolerance):
        return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1, color2))
    
    def convert_image(self, jpg_path):
        try:
            # Generate output path
            output_path = os.path.splitext(jpg_path)[0] + '.png'
            
            # Open image
            image = Image.open(jpg_path)
            image = image.convert('RGBA')
            
            # Get image data
            data = image.getdata()
            
            # Create new data with transparency
            new_data = []
            for item in data:
                # Check if the color is similar to the transparency color
                if self.is_similar_color(item[:3], self.transparency_color, self.tolerance):
                    new_data.append((item[0], item[1], item[2], 0))  # Make transparent
                else:
                    new_data.append(item)  # Keep original color
            
            # Update image with new data
            image.putdata(new_data)
            
            # Save as PNG
            image.save(output_path, 'PNG')
            
            messagebox.showinfo(
                "Success",
                f"Image converted successfully!\nSaved as: {output_path}"
            )
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"An error occurred while converting the image:\n{str(e)}"
            )

def main():
    root = tk.Tk()
    app = ImageConverterApp(root)
    
    # Handle window close button
    root.protocol("WM_DELETE_WINDOW", app.quit_app)
    
    root.mainloop()

if __name__ == "__main__":
    main()