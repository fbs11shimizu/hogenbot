import os
# import httpx
import streamlit as st
# import pandas as pd
# from typing import List

st.title('Streamlit')
st.header('Hello World')
st.text('streamlit初心者です')

# def format_results(result_files: List[str]) -> pd.DataFrame:
#     job_indices, filenames = [], []
#     for _, job_id, filename in map(lambda s: s.split('/'), result_files):
#         job_indices.append(job_id)
#         filenames.append(filename)
#     df = pd.DataFrame({'job_id': job_indices, 'filename': filenames})
#     return df


# API_HOST = os.environ.get('API_HOST', '127.0.0.1:80')



# if len(image_files) > 0 and st.button('Submit'):
#     files = [('files', file) for file in image_files]

#     r = httpx.post(f'http://{API_HOST}/predict', files=files)
#     st.success(r.json())


# if st.button('Refresh'):
#     st.success('Refreshed')
    
# r = httpx.get(f'http://{API_HOST}/results')
# df_results = format_results(r.json())
# st.write(df_results)