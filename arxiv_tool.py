import requests
import xml.etree.ElementTree as ET

# Step 1: Access the arXiv API
def search_arxive_paper(topic: str, max_results: int = 5) -> dict:
    query = "+".join(topic.lower().split())
    for char in list(' ()"'):
        if char in query:
            print(f"Invalid character '{char}' in query: {query}")
            raise ValueError(f"Character '{char}' not allowed in query")
    
    url = (
        "http://export.arxiv.org/api/query"
        f"?search_query=all:{query}"
        f"&max_results={max_results}"
        "&sortBy=submittedDate"
        "&sortOrder=descending"
    )
    print("Making request to URL:", url)
    response = requests.get(url)
    if not response.ok:
        print(f"ArXiv API request failed with status code {response.status_code}")
        raise ValueError(f"Bad response from API: {response}\n{response.text}")
    
    data = parse_arxive_xml(response.text)
    return data

# Step 2: Parse the XML response
def parse_arxive_xml(xml_data: str) -> dict:
    """ Parse the XML data from arXiv API and extract relevant information. """
    entries = []
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom"
    }
    root = ET.fromstring(xml_data)

    # Loop through each entry in atom namespace
    for entry in root.findall("atom:entry", ns):
        # Extract authors
        authors = [
            author.findtext("atom:name", namespaces=ns)
            for author in entry.findall("atom:author", ns)
        ]

        # Extract categories
        categories = [
            cat.attrib.get("term")
            for cat in entry.findall("atom:category", ns)
        ]

        # Extract PDF link
        pdf_link = None
        for link in entry.findall("atom:link", ns):
            if link.attrib.get("type") == "application/pdf":
                pdf_link = link.attrib.get("href")
                break

        entries.append({
            "title": entry.findtext("atom:title", namespaces=ns),
            "summary": entry.findtext("atom:summary", namespaces=ns).strip(),
            "authors": authors,
            "categories": categories,
            "pdf": pdf_link
        })
    return {"entries": entries}

# Test it



# step3 : convert into a tool
from langchain.tools import tool

@tool
def arxive_search(topic:str)->list[dict]:
    """Search for recenty papers

    Args:
        topic : str : topic to search for papers about

    Returns:
        list of papers with title, summary, authors, categories, and pdf link
    
    """
    print("Arxive Agent called")
    print(f"Searching for papers on topic: {topic}")
    papers=search_arxive_paper(topic)
    if(len(papers)==0):
        print("No papers found for topic:", topic)
        raise ValueError("No papers found for topic:", topic)
    print(f"Found {len(papers['entries'])} papers for topic: {topic}")
    return papers

    

