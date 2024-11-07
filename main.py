import os
import shutil
from datetime import datetime
import logging


class FileOrganizer:
    """A class to organize files in a directory based on their extensions."""

    def __init__(self, source_dir):
        """
        Initialize the FileOrganizer with a source directory.

        Args:
            source_dir (str): The directory path to organize
        """
        self.source_dir = source_dir
        self.extension_mapping = {
            # Images
            '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images',
            '.gif': 'Images', '.bmp': 'Images',

            # Documents
            '.pdf': 'Documents', '.doc': 'Documents', '.docx': 'Documents',
            '.txt': 'Documents', '.rtf': 'Documents', '.odt': 'Documents',

            # Audio
            '.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio',
            '.m4a': 'Audio', '.aac': 'Audio',

            # Video
            '.mp4': 'Video', '.avi': 'Video', '.mkv': 'Video',
            '.mov': 'Video', '.wmv': 'Video',

            # Archives
            '.zip': 'Archives', '.rar': 'Archives', '.7z': 'Archives',
            '.tar': 'Archives', '.gz': 'Archives',

            # Code
            '.py': 'Code', '.java': 'Code', '.cpp': 'Code',
            '.html': 'Code', '.css': 'Code', '.js': 'Code'
        }

        # Set up logging
        logging.basicConfig(
            filename='file_organizer.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def setup_directories(self):
        """Create necessary directories if they don't exist."""
        for directory in set(self.extension_mapping.values()):
            new_dir = os.path.join(self.source_dir, directory)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
                logging.info(f"Created directory: {new_dir}")

    def organize_files(self):
        """
        Organize files in the source directory based on their extensions.
        Returns a dictionary with statistics about the organization process.
        """
        stats = {
            'files_moved': 0,
            'errors': 0,
            'skipped': 0
        }

        try:
            self.setup_directories()

            # Iterate through all files in the source directory
            for filename in os.listdir(self.source_dir):
                if os.path.isfile(os.path.join(self.source_dir, filename)):
                    try:
                        # Get the file extension
                        file_ext = os.path.splitext(filename)[1].lower()

                        # Skip if the file is the log file
                        if filename == 'file_organizer.log':
                            continue

                        # Determine the destination directory
                        if file_ext in self.extension_mapping:
                            destination_dir = os.path.join(
                                self.source_dir,
                                self.extension_mapping[file_ext]
                            )

                            # Move the file
                            source_path = os.path.join(self.source_dir, filename)
                            destination_path = os.path.join(destination_dir, filename)

                            # Handle duplicate filenames
                            if os.path.exists(destination_path):
                                base, extension = os.path.splitext(filename)
                                new_filename = f"{base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"
                                destination_path = os.path.join(destination_dir, new_filename)

                            shutil.move(source_path, destination_path)
                            logging.info(f"Moved {filename} to {destination_dir}")
                            stats['files_moved'] += 1
                        else:
                            logging.info(f"Skipped {filename} - unknown extension")
                            stats['skipped'] += 1

                    except Exception as e:
                        logging.error(f"Error processing {filename}: {str(e)}")
                        stats['errors'] += 1

            return stats

        except Exception as e:
            logging.error(f"Major error during organization: {str(e)}")
            raise

    def get_organization_summary(self):
        """
        Generate a summary of the current organization state.
        Returns a dictionary with counts of files in each category.
        """
        summary = {}
        for directory in set(self.extension_mapping.values()):
            dir_path = os.path.join(self.source_dir, directory)
            if os.path.exists(dir_path):
                file_count = len([f for f in os.listdir(dir_path)
                                  if os.path.isfile(os.path.join(dir_path, f))])
                summary[directory] = file_count
        return summary


def main():
    # Get the directory path from user
    source_dir = input("Enter the directory path to organize: ").strip()

    # Validate the directory path
    if not os.path.exists(source_dir):
        print("Error: Directory does not exist!")
        return

    # Create and run the organizer
    try:
        organizer = FileOrganizer(source_dir)
        print("\nStarting file organization...")

        # Organize the files
        stats = organizer.organize_files()

        # Print results
        print("\nOrganization complete!")
        print(f"Files moved: {stats['files_moved']}")
        print(f"Files skipped: {stats['skipped']}")
        print(f"Errors encountered: {stats['errors']}")

        # Print current organization summary
        print("\nCurrent organization summary:")
        summary = organizer.get_organization_summary()
        for category, count in summary.items():
            print(f"{category}: {count} files")

    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        print("Check the log file for details.")


if __name__ == "__main__":
    main()