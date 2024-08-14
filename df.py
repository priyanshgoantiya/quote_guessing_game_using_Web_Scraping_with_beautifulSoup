import pandas as pd
df = pd.read_csv('Books.csv', header=None, names=['Price', 'Title'])

# Display the DataFrame (optional, for debugging)
print(df)

# Save DataFrame to a new CSV file
df.to_csv(r'C:\Users\Admin\Desktop\books.csv', index=True)