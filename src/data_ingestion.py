"""Data ingestion pipeline for Hadith and Quran JSON files."""

import json
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm


class Document:
    """Document with content and metadata."""
    
    def __init__(self, content: str, metadata: Dict[str, Any]):
        self.page_content = content
        self.metadata = metadata


class DataIngestion:
    """Load and process Hadith and Quran data from JSON files."""
    
    def __init__(self, data_path: Path):
        self.data_path = data_path
        self.documents: List[Document] = []
    
    def load_hadith_collection(self, collection_name: str) -> List[Document]:
        """Load a single Hadith collection from JSON file.
        
        Args:
            collection_name: Name of the collection (e.g., 'bukhari', 'muslim')
            
        Returns:
            List of Document objects with Hadith content and metadata
        """
        file_path = self.data_path / "ahadees" / f"{collection_name}.json"
        
        if not file_path.exists():
            print(f"Warning: {file_path} not found, skipping...")
            return []
        
        documents = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract collection metadata
        collection_title = data.get('metadata', {}).get('english', {}).get('title', collection_name.title())
        
        # Process each hadith directly from the hadiths array
        for hadith in tqdm(data.get('hadiths', []), desc=f"Processing {collection_title}"):
            # Create rich content combining English and Arabic
            content_parts = []
            
            # Get English text from the 'english' object
            english_obj = hadith.get('english', {})
            if isinstance(english_obj, dict):
                narrator = english_obj.get('narrator', '')
                english_text = english_obj.get('text', '')
                
                if narrator:
                    content_parts.append(f"Narrator: {narrator}")
                if english_text:
                    content_parts.append(f"English: {english_text}")
            
            # Add Arabic text
            arabic_text = hadith.get('arabic', '')
            if arabic_text:
                content_parts.append(f"Arabic: {arabic_text}")
            
            if not content_parts:
                continue
                
            # Combine into single content
            content = "\n\n".join(content_parts)
            
            # Find chapter info - get chapterId and look it up
            chapter_id = hadith.get('chapterId', '')
            chapter_title = 'Unknown Chapter'
            
            # Try to find the chapter in the chapters array
            for chapter in data.get('chapters', []):
                if chapter.get('id') == chapter_id:
                    chapter_title = chapter.get('english', 'Unknown Chapter')
                    break
            
            # Create metadata
            metadata = {
                'source_type': 'hadith',
                'collection': collection_title,
                'chapter': chapter_title,
                'hadith_id': str(hadith.get('id', 'unknown')),
                'narrator': english_obj.get('narrator', 'Unknown') if isinstance(english_obj, dict) else 'Unknown',
            }
            
            documents.append(Document(content=content, metadata=metadata))
        
        return documents
    
    def load_all_hadith_collections(self) -> List[Document]:
        """Load all Hadith collections from the ahadees directory.
        
        Returns:
            List of all Hadith documents
        """
        collections = [
            'bukhari', 'muslim', 'abudawud', 'tirmidhi',
            'nasai', 'ibnmajah', 'malik', 'ahmed', 'darimi'
        ]
        
        all_documents = []
        
        for collection in collections:
            docs = self.load_hadith_collection(collection)
            all_documents.extend(docs)
            print(f"✓ Loaded {len(docs)} hadiths from {collection.title()}")
        
        return all_documents
    
    def load_quran(self) -> List[Document]:
        """Load Quran verses from JSON file.
        
        Returns:
            List of Document objects with Quran verses
        """
        file_path = self.data_path / "quran" / "quran_en.json"
        
        if not file_path.exists():
            print(f"Warning: {file_path} not found, skipping...")
            return []
        
        documents = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Check if data is a list or dict
        surahs = data if isinstance(data, list) else data.get('surahs', [])
        
        # Process each surah
        for surah in tqdm(surahs, desc="Processing Quran"):
            surah_number = surah.get('number', surah.get('id', 0))
            surah_name = surah.get('name', surah.get('englishName', f'Surah {surah_number}'))
            
            # Process each verse
            verses = surah.get('verses', surah.get('ayahs', []))
            for verse in verses:
                verse_number = verse.get('number', verse.get('numberInSurah', 0))
                
                # Create content with English (and Arabic if available)
                content_parts = []
                
                english_text = verse.get('text', verse.get('translation', ''))
                if english_text:
                    content_parts.append(f"English: {english_text}")
                
                arabic_text = verse.get('arabic', verse.get('text_ar', ''))
                if arabic_text:
                    content_parts.append(f"Arabic: {arabic_text}")
                
                if not content_parts:
                    continue
                    
                content = "\n\n".join(content_parts)
                
                # Create metadata
                metadata = {
                    'source_type': 'quran',
                    'surah_number': surah_number,
                    'surah_name': surah_name,
                    'verse_number': verse_number,
                    'reference': f"{surah_name} {surah_number}:{verse_number}"
                }
                
                documents.append(Document(content=content, metadata=metadata))
        
        print(f"✓ Loaded {len(documents)} verses from Quran")
        return documents
    
    def load_all_data(self) -> List[Document]:
        """Load all data (Hadith collections + Quran).
        
        Returns:
            Complete list of all documents
        """
        print("\n📚 Starting data ingestion...\n")
        
        # Load Hadith
        hadith_docs = self.load_all_hadith_collections()
        
        # Load Quran
        quran_docs = self.load_quran()
        
        # Combine all documents
        self.documents = hadith_docs + quran_docs
        
        print(f"\n✅ Total documents loaded: {len(self.documents)}")
        print(f"   - Hadith: {len(hadith_docs)}")
        print(f"   - Quran: {len(quran_docs)}")
        
        return self.documents
