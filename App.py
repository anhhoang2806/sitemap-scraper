import streamlit as st
import requests
from xml.etree import ElementTree as ET
import pandas as pd

# Title
st.title('Sitemap Scraper')

# Input Field for Sitemap URL
sitemap_url = st.text_input('Enter the URL of your Sitemap:', '')

if sitemap_url:
    try:
        # Fetch the Sitemap
        response = requests.get(sitemap_url)
        if response.status_code == 200:
            # Parse the XML Sitemap
            tree = ET.ElementTree(ET.fromstring(response.content))
            root = tree.getroot()

            # Extract URLs
            urls = []
            for element in root.iter():
                if element.tag.endswith('loc'):
                    urls.append(element.text)

            # Display URLs
            if urls:
                st.success(f'Found {len(urls)} URLs in the sitemap.')
                df = pd.DataFrame(urls, columns=['URLs'])
                st.dataframe(df)

                # Download as CSV
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label='Download URLs as CSV',
                    data=csv,
                    file_name='sitemap_urls.csv',
                    mime='text/csv',
                )
            else:
                st.warning('No URLs found in the sitemap.')

        else:
            st.error(f'Failed to fetch sitemap. HTTP Status Code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        st.error(f'Error fetching the sitemap: {e}')
    except ET.ParseError:
        st.error('Error parsing the XML file. Please check if the URL points to a valid XML sitemap.')

