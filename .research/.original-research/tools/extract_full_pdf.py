#!/usr/bin/env python3

import os
import io
import sys
import re
import traceback
from pdfminer.high_level import extract_text
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from datetime import datetime
import pytesseract
from pdf2image import convert_from_path
import tempfile
import argparse

# Create output directory if it doesn't exist
output_dir = ".research/pdf_extracts"
os.makedirs(output_dir, exist_ok=True)

# Front matter data 
front_matter = {
    "3567029.pdf": {
        "title": "White Ethnogenesis and Gradual Capitalism: Perspectives from Colonial Archaeological Sites in the Chesapeake",
        "creator": "Alison Bell",
        "date": "September 2005",
        "format": "Journal Article",
        "subject": "Colonial archaeology and ethnogenesis in the Chesapeake region",
        "identifier": "3567029",
        "source": "American Anthropologist, Vol. 107, No. 3 (Sep., 2005), pp. 446-460",
        "topics": "archaeology, ethnogenesis, capitalism, colonialism, Chesapeake, historical archaeology, White identity"
    },
    "23018406 (1).pdf": {
        "title": "The Archaeology of Native Societies in the Chesapeake: New Investigations and Interpretations",
        "creator": "Martin Gallivan",
        "date": "September 2011",
        "format": "Journal Article",
        "subject": "Archaeological research on Native American societies in the Chesapeake region",
        "identifier": "23018406",
        "source": "Journal of Archaeological Research, Vol. 19, No. 3 (September 2011), pp. 281-325",
        "topics": "archaeology, Native American societies, Chesapeake, Middle Atlantic region, prehistory, colonial contact, research synthesis, archaeological interpretations"
    },
    "25096728.pdf": {
        "title": "Adaptation and Innovation: Archaeological and Architectural Perspectives on the Seventeenth-Century Chesapeake",
        "creator": "Willie Graham, Carter L. Hudgins, Carl R. Lounsbury, Fraser D. Neiman, and James P. Whittenburg",
        "date": "2007",
        "format": "Journal Article",
        "subject": "Archaeological and architectural analysis of the Chesapeake in the 17th century",
        "identifier": "25096728",
        "source": "The William and Mary Quarterly, 64(3), 451-522",
        "topics": "archaeology, architecture, Chesapeake region, colonial buildings, seventeenth-century, material culture, settlement patterns, vernacular architecture"
    },
    "2773073.pdf": {
        "title": "From Organization to Society: Virginia in the Seventeenth Century",
        "creator": "Sigmund Diamond",
        "date": "1958",
        "format": "Journal Article",
        "subject": "Social and organizational development in colonial Virginia",
        "identifier": "2773073",
        "source": "American Journal of Sociology, 63(5), 457-475",
        "topics": "colonial Virginia, social organization, seventeenth-century, sociological analysis, institutional development, social structure"
    },
    "willmaryquar.68.3.0361.pdf": {
        "title": "The Visible Fist: The Chesapeake Tobacco Trade in War and the Purpose of Empire, 1690-1715",
        "creator": "Douglas Bradburn",
        "date": "2011",
        "format": "Journal Article",
        "subject": "Analysis of the Chesapeake tobacco trade during wartime",
        "identifier": "10.5309/willmaryquar.68.3.0361",
        "source": "The William and Mary Quarterly, 68(3), 361-386",
        "topics": "tobacco trade, Chesapeake, colonial commerce, British Empire, warfare, commercial regulation, 1690-1715"
    },
    "4248939 (1).pdf": {
        "title": "The Invasion of Virginia: Indians, Colonialism, and the Conquest of Cant: A Review Essay on Anglo-Indian Relations in the Chesapeake",
        "creator": "J. Frederick Fausz",
        "date": "1987",
        "format": "Journal Article",
        "subject": "Review essay on Anglo-Indian relations in colonial Chesapeake",
        "identifier": "4248939",
        "source": "The Virginia Magazine of History and Biography, 95(2), 133-156",
        "topics": "Native Americans, colonialism, Chesapeake region, Virginia, Anglo-Indian relations, historiography, colonial encounters"
    },
    "1493424.pdf": {
        "title": "Notes on the Evolution of Virginia Brickwork from the Seventeenth Century to the Late Nineteenth Century",
        "creator": "Calder Loth",
        "date": "1974",
        "format": "Journal Article",
        "subject": "Historical analysis of Virginia brickwork evolution",
        "identifier": "10.2307/1493424",
        "source": "Bulletin of the Association for Preservation Technology, 6(2), 82-120",
        "topics": "architectural history, brickwork, Virginia, building construction, historic preservation, material culture, masonry techniques"
    },
    "25470524.pdf": {
        "title": "Archaeobotanical Analysis and Interpretations of Enslaved Virginian Plant Use at Rich Neck Plantation (44WB52)",
        "creator": "Stephen A. Mrozowski, Maria Franklin, and Leith Hunt",
        "date": "2008",
        "format": "Journal Article",
        "subject": "Archaeobotanical analysis of plant use by enslaved people at Rich Neck Plantation",
        "identifier": "25470524",
        "source": "American Antiquity, 73(4), 699-728",
        "topics": "archaeobotany, slavery, Virginia, Rich Neck Plantation, plant use, colonial archaeology, foodways, ethnobotany"
    },
    "4245672.pdf": {
        "title": "Seventeenth Century Brickmaking and Tilemaking at Jamestown, Virginia",
        "creator": "J. C. Harrington",
        "date": "1950",
        "format": "Journal Article",
        "subject": "Study of brick and tile manufacturing in colonial Jamestown",
        "identifier": "4245672",
        "source": "The Virginia Magazine of History and Biography, 58(1), 16-39",
        "topics": "Jamestown, brickmaking, tilemaking, colonial construction, architectural history, archaeological evidence, building materials"
    },
    "24572697.pdf": {
        "title": "Health Consequences of Contact on Two Seventeenth-Century Native Groups from the Mid-Atlantic Region of Maryland",
        "creator": "Sara K. Becker",
        "date": "December 2013",
        "format": "Journal Article",
        "subject": "Native American health changes during colonial contact in Maryland",
        "identifier": "24572697",
        "source": "International Journal of Historical Archaeology, Vol. 17, No. 4 (December 2013), pp. 713-730",
        "topics": "archaeology, bioarchaeology, Native American health, colonial contact, Maryland, 17th century, paleopathology, European contact"
    },
    "40914371.pdf": {
        "title": "Comparison of Late Woodland Cultures: Delaware, Potomac, and Susquehanna River Valleys, Middle Atlantic Region",
        "creator": "R. Michael Stewart",
        "date": "Fall 1993",
        "format": "Journal Article",
        "subject": "Late Woodland cultures in the Middle Atlantic region",
        "identifier": "40914371",
        "source": "Archaeology of Eastern North America, Vol. 21 (Fall 1993), pp. 163-178",
        "topics": "archaeology, prehistory, Middle Atlantic region, Late Woodland period, Delaware River Valley, Potomac River Valley, Susquehanna River Valley, comparative analysis"
    },
    "40914397.pdf": {
        "title": "Archaeological Article - 40914397",
        "creator": "Unknown",
        "date": "Unknown",
        "format": "Journal Article",
        "subject": "Archaeology",
        "identifier": "40914397",
        "source": "Archaeology of Eastern North America",
        "topics": "archaeology, prehistory, Eastern North America"
    },
    "40914306 (1).pdf": {
        "title": "Trade and Exchange in Middle Atlantic Region Prehistory",
        "creator": "R. Michael Stewart",
        "date": "Fall 1989",
        "format": "Journal Article",
        "subject": "Prehistoric trade and exchange in the Middle Atlantic region",
        "identifier": "40914306",
        "source": "Archaeology of Eastern North America, Vol. 17 (Fall 1989), pp. 47-78",
        "topics": "archaeology, prehistory, Middle Atlantic region, trade networks, exchange systems, Late Archaic, Woodland period"
    },
    "Falls Church City Schools A History (1999).pdf": {
        "title": "Falls Church City Schools: A History",
        "creator": "Falls Church City Public Schools",
        "date": "1999",
        "format": "Books",
        "subject": "Falls Church City Public Schools",
        "identifier": "Falls Church City Schools A History (1999)",
        "source": "https://archive.mrspl.org/Documents/Detail/falls-church-city-schools-a-history/39063",
        "topics": "Falls Church history, education, schools, public schools, history"
    },
    "Falls Church _Virginia Village Revisited.pdf": {
        "title": "Falls Church: A Virginia Village Revisited",
        "creator": "Unknown", # Can be updated if known
        "date": "Unknown", # Can be updated if known
        "format": "Books",
        "subject": "Falls Church, Virginia",
        "identifier": "Falls Church _Virginia Village Revisited",
        "source": "https://archive.mrspl.org/Documents/Detail/falls-church-a-virginia-village-revisited/38847",
        "topics": "Falls Church history, Virginia, local history"
    },
    "No 6 Ancient Washington.pdf": {
        "title": "Ancient Washington",
        "creator": "Unknown",
        "date": "Unknown",
        "format": "Document",
        "subject": "Washington, D.C. history",
        "identifier": "No 6 Ancient Washington",
        "source": "Local archive",
        "topics": "Washington history, DC history, local history"
    },
    "archeological_overview.pdf": {
        "title": "Archaeological Overview and Assessment of Native American Heritage in Falls Church Region",
        "creator": "Archaeological Research Team",
        "date": "2023",
        "format": "Research Report",
        "subject": "Indigenous archaeology of Falls Church and surrounding regions",
        "identifier": "Archaeological Overview and Assessment",
        "source": "Falls Church Historical Committee",
        "topics": "Native American archaeology, Falls Church history, indigenous heritage, Little Falls region, Potomac Valley archaeology"
    },
    "SiteReportPfanstiehlBloxhamCemeteryAX127and128PreliminaryAssessment.pdf": {
        "title": "Preliminary Archaeological Assessment: Alexandria Business Center, Alexandria, Virginia",
        "creator": "Cynthia Pfanstiehl, Edward Otter, Marilyn Harper",
        "date": "July 1989",
        "format": "Research Report",
        "subject": "Archaeological assessment of Alexandria Business Center",
        "identifier": "SiteReportPfanstiehlBloxhamCemeteryAX127and128PreliminaryAssessment",
        "source": "Engineering-Science, Inc., 1133 Fifteenth Street, N.W., Washington, D.C. 20005",
        "topics": "Alexandria archaeology, Virginia archaeology, historical sites, archaeological assessment"
    },
    "rapidan_mound.pdf": {
        "title": "Collective Burial in Late Prehistoric Virginia: Excavation and Analysis of the Rapidan Mound",
        "creator": "Gary H. Dunham, Debra L. Gold, and Jeffrey L. Hantman",
        "date": "2003",
        "format": "Journal Article",
        "subject": "Virginia archaeology, Monacan, burial mounds",
        "identifier": "10.2307/3557035",
        "source": "American Antiquity, 68(1), 109-128",
        "topics": "Virginia archaeology, Monacan, Siouan, burial mounds, Late Woodland period, mortuary practices, Piedmont region"
    },
    "3557035.pdf": {
        "title": "Collective Burial in Late Prehistoric Virginia: Excavation and Analysis of the Rapidan Mound",
        "creator": "Gary H. Dunham, Debra L. Gold, and Jeffrey L. Hantman",
        "date": "2003",
        "format": "Journal Article",
        "subject": "Virginia archaeology, Monacan, burial mounds",
        "identifier": "10.2307/3557035",
        "source": "American Antiquity, 68(1), 109-128",
        "topics": "Virginia archaeology, Monacan, Siouan, burial mounds, Late Woodland period, mortuary practices, Piedmont region"
    },
    "40066884.pdf": {
        "title": "The Historic Potomac River",
        "creator": "Langley, Susan B. M.",
        "date": "1995",
        "format": "Journal Article",
        "subject": "Historical and archaeological study of the Potomac River",
        "identifier": "40066884",
        "source": "Maryland Historical Magazine, Vol. 90, No. 3 (1995), pp. 348-385",
        "topics": "Potomac River, historical archaeology, Maryland history, Virginia history, maritime history, colonial era, waterways"
    },
    "744246.pdf": {
        "title": "Gun Laws in Early America: The Regulation of Firearms Ownership, 1607-1794",
        "creator": "Michael A. Bellesiles",
        "date": "Autumn 1998",
        "format": "Journal Article",
        "subject": "Historical analysis of gun regulations in colonial America, with focus on Native American relations",
        "identifier": "744246",
        "source": "Law and History Review, Vol. 16, No. 3 (Autumn 1998), pp. 567-589",
        "topics": "gun laws, firearms regulation, colonial America, Native Americans, early American history, legal history, weapon trade, colonial security"
    },
    "25615569.pdf": {
        "title": "On the Archaeology of Early Canals: Research on the Patowmack Canal in Great Falls, Virginia",
        "creator": "Richard J. Dent",
        "date": "1986",
        "format": "Journal Article",
        "subject": "Archaeological research on the Patowmack Canal at Great Falls, Virginia",
        "identifier": "25615569",
        "source": "Historical Archaeology, Vol. 20, No. 1 (1986), pp. 50-62",
        "topics": "historical archaeology, Patowmack Canal, Great Falls, Virginia, George Washington, canal construction, transportation history, early American infrastructure"
    },
    "40067444.pdf": {
        "title": "Early Landmarks between Great Hunting Creek and the Falls of the Potomac",
        "creator": "Charles O. Paullin",
        "date": "1930",
        "format": "Journal Article",
        "subject": "Historical study of early landmarks along the Potomac River from Great Hunting Creek to the Falls",
        "identifier": "40067444",
        "source": "Records of the Columbia Historical Society, Washington, D.C., Vol. 31/32 (1930), pp. 53-79",
        "topics": "Potomac River, historical landmarks, Washington D.C. area, Great Hunting Creek, Falls of the Potomac, colonial geography, early settlements, historical geography"
    },
    "4241946.pdf": {
        "title": "Narrative of Bacon's Rebellion",
        "creator": "Unknown", 
        "date": "October 1896",
        "format": "Journal Article",
        "subject": "Historical account of Bacon's Rebellion in colonial Virginia",
        "identifier": "4241946",
        "source": "The Virginia Magazine of History and Biography, Vol. 4, No. 2 (Oct., 1896), pp. 117-154",
        "topics": "Bacon's Rebellion, colonial Virginia, Nathaniel Bacon, Governor William Berkeley, 17th century, American history, colonial uprisings, Virginia history"
    },
    "4248939.pdf": {
        "title": "The Invasion of Virginia. Indians, Colonialism, and the Conquest of Cant: A Review Essay on Anglo-Indian Relations in the Chesapeake",
        "creator": "J. Frederick Fausz",
        "date": "April 1987",
        "format": "Journal Article",
        "subject": "Review essay analyzing Anglo-Indian relations in the Chesapeake region during colonial period",
        "identifier": "4248939",
        "source": "The Virginia Magazine of History and Biography, Vol. 95, No. 2, \"The Takinge Upp of Powhatans Bones\": Virginia Indians, 1585-1945 (Apr., 1987), pp. 133-156",
        "topics": "Native Americans, Virginia Indians, Powhatan, colonial Virginia, Chesapeake region, Anglo-Indian relations, colonialism, historical revisionism"
    },
    "44286295.pdf": {
        "title": "Bacon's Rebellion in Indian Country",
        "creator": "James D. Rice",
        "date": "December 2014",
        "format": "Journal Article",
        "subject": "Historical analysis of Bacon's Rebellion from a Native American perspective",
        "identifier": "44286295",
        "source": "The Journal of American History, Vol. 101, No. 3 (December 2014), pp. 726-750",
        "topics": "Bacon's Rebellion, Native Americans, Virginia history, colonial conflict, Nathaniel Bacon, indigenous perspectives, Susquehannock, Occaneechi, Pamunkey"
    },
    "4247595.pdf": {
        "title": "The Causes of Bacon's Rebellion: Some Suggestions",
        "creator": "Warren M. Billings",
        "date": "October 1970",
        "format": "Journal Article",
        "subject": "Analysis of the causes and contributing factors to Bacon's Rebellion in colonial Virginia",
        "identifier": "4247595",
        "source": "The Virginia Magazine of History and Biography, Vol. 78, No. 4 (October 1970), pp. 409-435",
        "topics": "Bacon's Rebellion, colonial Virginia, Nathaniel Bacon, Sir William Berkeley, 17th century Virginia, political history, colonial governance, social conflict"
    },
    "41059478.pdf": {
        "title": "Bacon's Rebellion, the Grievances of the People, and the Political Culture of Seventeenth-Century Virginia",
        "creator": "Brent Tarter",
        "date": "2011",
        "format": "Journal Article",
        "subject": "Analysis of the political culture and public grievances that led to Bacon's Rebellion",
        "identifier": "41059478",
        "source": "The Virginia Magazine of History and Biography, Vol. 119, No. 1 (2011), pp. 2-41",
        "topics": "Bacon's Rebellion, colonial Virginia, political culture, public grievances, Nathaniel Bacon, Governor William Berkeley, colonial governance, representative government"
    },
    "pennhistory.88.3.0287.pdf": {
        "title": "The \"Four Nations of Indians Upon the Susquehanna\": Mid-Atlantic Murder, Diplomacy, and Political Identity, 1717–1723",
        "creator": "Paul Douglas Newman",
        "date": "Summer 2021",
        "format": "Journal Article",
        "subject": "Analysis of Native American diplomatic relations and political identity in the Mid-Atlantic region",
        "identifier": "pennhistory.88.3.0287",
        "source": "Pennsylvania History: A Journal of Mid-Atlantic Studies, Vol. 88, No. 3, Special Issue: Rethinking Pennsylvania's Eighteenth Century Borderlands (Summer 2021), pp. 287-318",
        "topics": "Native Americans, Susquehanna River, Mid-Atlantic region, diplomacy, colonial Pennsylvania, political identity, Iroquois, Conoy, Shawnee, Tuscarora"
    },
    "1006560.pdf": {
        "title": "The Massawomeck: Raiders and Traders into the Chesapeake Bay in the Seventeenth Century",
        "creator": "James F. Pendergast",
        "date": "1991",
        "format": "Journal Article",
        "subject": "Historical study of the Massawomeck Native American tribe and their interactions in the Chesapeake region",
        "identifier": "1006560",
        "source": "Transactions of the American Philosophical Society, Vol. 81, No. 2 (1991), pp. i-vii+1-101",
        "topics": "Massawomeck, Native Americans, Chesapeake Bay, 17th century, indigenous history, trade networks, Iroquois, Susquehannock, John Smith, colonial exploration"
    },
    "PROVISIONING EARLY AMERICAN TOWNS. THE CHESAPEAKE_ A MULTIDISCIPLINARY CASE STUDY FINAL PERFORMANCE REPORT _ Colonial Williamsburg Digital Library.pdf": {
        "title": "Provisioning Early American Towns. The Chesapeake: A Multidisciplinary Case Study",
        "creator": "Lorena S. Walsh, Ann Smart Martin, Joanne Bowen",
        "date": "30 September 1997",
        "format": "Research Report",
        "subject": "Final Performance Report on provisioning systems in early American Chesapeake towns",
        "identifier": "CW Research Report Series - 0404",
        "source": "Colonial Williamsburg Foundation Library, Williamsburg, Virginia, 1990",
        "topics": "colonial Chesapeake, urban provisioning, economic history, food systems, town development, multidisciplinary research, material culture, archaeology"
    },
    "45128189.pdf": {
        "title": "Reassessing the Hallowes Site: Conflict and Settlement in the Seventeenth-Century Potomac Valley",
        "creator": "D. Brad Hatch, Benjamin J. Heath, and Lauren K. McMillan",
        "date": "2014",
        "format": "Journal Article",
        "subject": "Historical archaeology of 17th-century Potomac Valley; reassessment of Hallowes Site",
        "identifier": "45128189",
        "source": "Historical Archaeology, Vol. 48, No. 4 (2014), pp. 46-75",
        "topics": "historical archaeology, Hallowes Site, Potomac Valley, conflict, settlement, seventeenth-century, colonial period"
    },
    "1922843.pdf": {
        "title": "The Seed from which Virginia Grew",
        "creator": "George Arents",
        "date": "1939",
        "format": "Journal Article",
        "subject": "Early colonial Virginia origins",
        "identifier": "1922843",
        "source": "The William and Mary College Quarterly Historical Magazine, Vol. 19, No. 2 (1939), pp. 124-129",
        "topics": "Virginia history, colonial Virginia, early settlement, Virginia Company, historical analysis"
    },
    "25615692.pdf": {
        "title": "\"The Bare Necessities\": Standards of Living in England and the Chesapeake, 1650-1700",
        "creator": "Janet P. P. Horn",
        "date": "1988",
        "format": "Journal Article",
        "subject": "Comparative analysis of living standards in 17th‑century England and the Chesapeake region",
        "identifier": "25615692",
        "source": "Historical Archaeology, Vol. 22, No. 2 (1988), pp. 74-91",
        "topics": "standards of living, England, Chesapeake, 17th century, historical archaeology, colonial period, economic history, consumer goods"
    },
    "597174.pdf": {
        "title": "Re‐creating Mount Vernon: The Virginia Building at the 1893 Chicago World's Columbian Exposition",
        "creator": "Lydia Mattice Brandt",
        "date": "2009",
        "format": "Journal Article",
        "subject": "Analysis of the Virginia Building at the 1893 Chicago World's Fair",
        "identifier": "597174", 
        "source": "Winterthur Portfolio, Vol. 43, No. 1 (2009), pp. 79-114",
        "topics": "Mount Vernon, World's Columbian Exposition, colonial revival, architecture, Virginia Building, architectural history"
    },
    "1181112.pdf": {
        "title": "The American Colonial Revival in the 1930s",
        "creator": "David Gebhard",
        "date": "1987",
        "format": "Journal Article",
        "subject": "Colonial Revival architecture and design during the 1930s",
        "identifier": "1181112",
        "source": "Winterthur Portfolio, Vol. 22, No. 2/3 (1987), pp. 109-148",
        "topics": "Colonial Revival, 1930s, architecture, design history, American architecture, Depression era"
    },
    "989087.pdf": {
        "title": "The Colonial Revival and American Nationalism",
        "creator": "William B. Rhoads",
        "date": "1976",
        "format": "Journal Article",
        "subject": "Analysis of Colonial Revival architecture in relation to American nationalism",
        "identifier": "989087",
        "source": "Journal of the Society of Architectural Historians, Vol. 35, No. 4 (1976), pp. 239-254",
        "topics": "Colonial Revival, American nationalism, architectural history, patriotism, historical architecture"
    },
    "1556905.pdf": {
        "title": "Random Reflections on the Colonial Revival",
        "creator": "Wayne Andrews",
        "date": "1964",
        "format": "Journal Article",
        "subject": "Reflections on the Colonial Revival movement in American architecture",
        "identifier": "1556905",
        "source": "Archives of American Art Journal, Vol. 4, No. 2 (1964), pp. 1-4",
        "topics": "Colonial Revival, architecture, American history, historical preservation, architectural movements"
    },
    "42620492.pdf": {
        "title": "The Discovery of America's Architectural Past, 1874-1914",
        "creator": "William B. Rhoads",
        "date": "1990",
        "format": "Journal Article",
        "subject": "Early documentation and discovery of American architectural history",
        "identifier": "42620492",
        "source": "Studies in the History of Art, Vol. 35 (1990), pp. 23-24",
        "topics": "American architecture, architectural history, historical documentation, preservation, colonial architecture"
    },
    "990566.pdf": {
        "title": "Beaux-Arts Ideals and Colonial Reality: The Reconstruction of Williamsburg's Capitol, 1928-1934",
        "creator": "Carl R. Lounsbury",
        "date": "1990",
        "format": "Journal Article",
        "subject": "Analysis of Colonial Williamsburg's Capitol reconstruction project",
        "identifier": "990566",
        "source": "Journal of the Society of Architectural Historians, Vol. 49, No. 4 (1990), pp. 373-389",
        "topics": "Colonial Williamsburg, Beaux-Arts, architectural reconstruction, historic preservation, Capitol building, colonial architecture"
    },
    "41730172.pdf": {
        "title": "Uncovering Early Colonial City Point, Virginia",
        "creator": "David G. Orr, Douglas Campana and Brooke S. Blades",
        "date": "May/June 1985",
        "format": "Journal Article",
        "subject": "Archaeological excavation of colonial City Point, Virginia",
        "identifier": "41730172",
        "source": "Archaeology, Vol. 38, No. 3 (May/June 1985), pp. 64-65, 78",
        "topics": "historical archaeology, Virginia history, City Point, colonial archaeology, archaeological excavation, urban archaeology"
    },
    "3557036.pdf": {
        "title": "Isotopic Evidence for Diet in the Seventeenth-Century Colonial Chesapeake",
        "creator": "Douglas H. Ubelaker and Douglas W. Owsley",
        "date": "January 2003",
        "format": "Journal Article",
        "subject": "Bioarchaeological analysis of diet in colonial Chesapeake using isotope analysis",
        "identifier": "3557036",
        "source": "American Antiquity, Vol. 68, No. 1 (Jan., 2003), pp. 129-139",
        "topics": "bioarchaeology, isotope analysis, diet, colonial Chesapeake, seventeenth-century, historical archaeology, human remains"
    },
    "1723 Stafford County Rent Roll .pdf": {
        "title": "1723 Stafford County Rent Roll",
        "creator": "Stafford County, Virginia",
        "date": "1723",
        "format": "Historical Document",
        "subject": "Colonial era tax and property records for Stafford County, Virginia",
        "identifier": "Stafford County Rent Roll 1723",
        "source": "Prince William County Government Archives",
        "topics": "colonial Virginia, Stafford County, rent rolls, property records, taxation, land ownership, colonial history"
    }
}

def extract_text_with_ocr(pdf_path, start_page=0, max_pages=None, batch_size=10):
    """Extract text from PDF using OCR, processing in batches to avoid memory issues"""
    print("Using OCR to extract text from scanned PDF...")
    
    all_text = ""
    current_page = start_page
    
    try:
        # Get total number of pages
        import subprocess
        result = subprocess.run(['pdfinfo', pdf_path], capture_output=True, text=True)
        pages_line = [line for line in result.stdout.split('\n') if 'Pages:' in line]
        if pages_line:
            total_pages = int(pages_line[0].split('Pages:')[1].strip())
            print(f"PDF has {total_pages} total pages")
        else:
            print("Couldn't determine total page count, will process until the end")
            total_pages = float('inf') if max_pages is None else (start_page + max_pages)
    except Exception as e:
        print(f"Error getting page count: {e}")
        total_pages = float('inf') if max_pages is None else (start_page + max_pages)
    
    while current_page < total_pages:
        if max_pages is not None and current_page >= start_page + max_pages:
            break
            
        end_page = min(current_page + batch_size, total_pages)
        print(f"Processing batch: pages {current_page+1} to {end_page}")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                # Convert PDF pages to images for this batch
                images = convert_from_path(
                    pdf_path, 
                    dpi=300, 
                    first_page=current_page+1, 
                    last_page=end_page
                )
                
                print(f"Converted {len(images)} pages to images")
                
                # Extract text from each image using OCR
                for i, image in enumerate(images):
                    page_num = current_page + i + 1
                    print(f"Processing page {page_num} with OCR...")
                    
                    page_text = pytesseract.image_to_string(image)
                    all_text += f"\n\n=== Page {page_num} ===\n\n"
                    all_text += page_text
                    
                # Move to next batch
                current_page = end_page
                
            except Exception as e:
                print(f"Error in OCR extraction batch: {e}")
                traceback.print_exc()
                # Try to continue with next batch
                current_page = end_page
    
    return all_text

def process_pdf(pdf_path, filename, args):
    print(f"Processing {filename}...")
    
    # For scanned PDFs that need OCR
    if args.ocr:
        print("Using OCR method directly as specified...")
        text = extract_text_with_ocr(pdf_path, start_page=args.start_page, max_pages=args.max_pages)
    else:
        # First try the standard extraction method
        text = extract_text(pdf_path)
        
        # If we didn't get much text, try OCR
        if len(text.strip()) < 100:
            print(f"Standard extraction yielded little text, trying OCR...")
            text = extract_text_with_ocr(pdf_path, start_page=args.start_page, max_pages=args.max_pages)
    
    # Post-process text to remove duplicate consecutive lines
    text = remove_duplicate_lines(text)
    
    # Get frontmatter for this file
    metadata = front_matter.get(filename, {})
    if not metadata:
        print(f"Warning: No front matter found for {filename}, generating basic front matter")
        # Generate basic front matter
        base_name = os.path.splitext(filename)[0]
        metadata = {
            "title": f"Extracted PDF: {base_name}",
            "creator": "Unknown",
            "date": datetime.now().strftime('%Y-%m-%d'),
            "format": "PDF Extract",
            "subject": f"Content extracted from {filename}",
            "identifier": base_name,
            "source": pdf_path,
            "topics": "PDF extract, document analysis"
        }
    
    # Create frontmatter in markdown format
    front_matter_md = "---\n"
    for key, value in metadata.items():
        front_matter_md += f"{key}: \"{value}\"\n"
    front_matter_md += f"type: \"book extract\"\n"
    front_matter_md += f"extract_date: \"{datetime.now().strftime('%Y-%m-%d')}\"\n"
    front_matter_md += "---\n\n"
    
    # Combine frontmatter and text
    full_content = front_matter_md + text
    
    # Create sanitized filename for output
    output_base = os.path.splitext(filename)[0].replace(" ", "-").lower()
    
    # Add suffix for partial extracts
    if args.max_pages is not None:
        end_page = args.start_page + args.max_pages
        output_filename = f"{output_base}-pages-{args.start_page+1}-to-{end_page}.md"
    else:
        output_filename = f"{output_base}-full.md"
        
    output_path = os.path.join(output_dir, output_filename)
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"Saved to {output_path}")
    print(f"Extracted text length: {len(text)} characters")
    return output_path

def remove_duplicate_lines(text):
    """Remove duplicate consecutive lines from text"""
    lines = text.split('\n')
    result_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        result_lines.append(line)
        
        # Skip duplicate consecutive lines
        while i + 1 < len(lines) and lines[i + 1] == line:
            i += 1
        
        i += 1
    
    return '\n'.join(result_lines)

def main():
    parser = argparse.ArgumentParser(description='Extract text from PDF files with OCR')
    parser.add_argument('--pdf', help='Specific PDF file to process')
    parser.add_argument('--ocr', action='store_true', help='Force OCR processing')
    parser.add_argument('--start-page', type=int, default=0, help='Starting page (0-indexed)')
    parser.add_argument('--max-pages', type=int, help='Maximum number of pages to process')
    args = parser.parse_args()
    
    pdf_dir = ".research/pdfs"
    
    if args.pdf:
        # Process a single PDF
        pdf_path = args.pdf if os.path.isabs(args.pdf) else os.path.join(pdf_dir, args.pdf)
        if not os.path.exists(pdf_path):
            print(f"Error: File {pdf_path} not found")
            return
        filename = os.path.basename(pdf_path)
        output_path = process_pdf(pdf_path, filename, args)
        print(f"Output file: {output_path}")
    else:
        # Process all PDFs in the directory
        for filename in os.listdir(pdf_dir):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(pdf_dir, filename)
                process_pdf(pdf_path, filename, args)

if __name__ == "__main__":
    main() 