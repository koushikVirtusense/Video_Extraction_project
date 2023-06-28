from labelbox import Client, Dataset


# Create a Labelbox client
client = Client(api_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJjbGZpdG1rZmsxMGc2MDd4dTAzaTU1dXk2Iiwib3JnYW5pemF0aW9uSWQiOiJja2l2enNpMXR5cmNvMDc0MWczbXEwaGtwIiwiYXBpS2V5SWQiOiJjbGlrYWNncGIwYThqMDd3emZzczczOXJrIiwic2VjcmV0IjoiNTU2OWU1OGNmYmFiMTE4OTY1NmFjZTQ2MWEyNmJkZDAiLCJpYXQiOjE2ODYwNTYyMjksImV4cCI6MjMxNzIwODIyOX0.lW7RRRuqGvi6--1hIDf08h62-rKaHT2wBwSElKQgDkw')

# Define the dataset names
dataset_names = ['10083025', '10083026', '10083027','10083028','10083029','10083030','10083031','10083032','10083033',
                 '10083034','10083035','10083036','10083037','10083038','10083039','10083040','10083041','10083042','10083043','10083044','10083045']  # Replace with your dataset IDs

# Create an empty list to store the data rows
all_data_rows = []

# Loop through the dataset names
for dataset_name in dataset_names:
    # Get the datasets with matching names
    datasets = client.get_datasets(where=Dataset.name == dataset_name)
    for dataset in datasets:
        # Get the data rows from the dataset
        data_rows = dataset.data_rows()
        #print(data_rows.name)

        # Add the data rows to the list
        all_data_rows.extend(data_rows)

# Check if there are any data rows
if len(all_data_rows) > 0:
    # Process the data rows or create a batch in the project
    # Example: Create a batch with the data rows in a project
    project_id = 'clfis09as04ry07v7c48t0et5'  # Replace with your project ID
    project = client.get_project(project_id)
    batch_name = 'New Batch1'  # Provide a name for the batch
    batch = project.create_batch(name=batch_name, data_rows=all_data_rows)

    print(f'Created a new batch with {len(all_data_rows)} data rows in project {project.name}.')
else:
    print('No data rows found. Unable to create a batch.')
