# Multimodal_Leukemia_Description_Generation
This project explores the use of **Vision-Language Models (VLMs)** for generating interpretable morphological descriptions of blood smear images for leukemia diagnosis. The system uses CLIP (zero-shot and LoRA-tuned) and GPT-3.5 to generate textual outputs that mimic expert-written descriptions from hematology atlases. The reccomended IDE is Google Colab, so there is no requirements file. 

## Repository Structure

| File/Folder                  | Description |
|-----------------------------|-------------|
| `FYP1.ipynb`                | Main notebook: preprocessing, CLIP feature extraction, and description generation |
| `FYP1_LoRA_Tuning.ipynb`    | LoRA fine-tuning notebook for CLIP encoder using PEFT |
| `main.py`                   | File to extract images and descriptions from Mindray Atlas |
| `aml_image_metadata.csv`    | Metadata with image paths, class labels, and abbreviations |
| `blood-cells-atlas.pdf`     | Reference source for morphological descriptions |
| `AML-Atlas-*.zip`           | Archive of extracted reference images and descriptions from Mindray|
| `README.md`                 | This file |

---

## Setup Instructions

1. Clone the repo:
```bash
git clone https://github.com/pmchhaya/Multimodal_Leukemia_Description_Generation.git
cd Multimodal_Leukemia_Description_Generation
```

2. Open `FYP1.ipynb` in **Google Colab** (recommended for GPU access).

3. Add your OpenAI API key if using GPT-3.5, replace existing API key with new one:
```python
openai.api_key = "YOUR_API_KEY"
```
4. Full AML dataset can be found here: https://www.cancerimagingarchive.net/collection/aml-cytomorphology_lmu/
---

##  How to Run

###  1. `FYP1.ipynb`  
Performs CLIP-based feature extraction, descriptor generation, and description output via:
- Template (rule-based)
- LoRA-tuned template
- GPT-3.5 generated paragraph

###  2. `FYP1_LoRA_Tuning.ipynb`  
Fine-tunes the CLIP vision encoder using Low-Rank Adaptation (LoRA). Produces:
- `lora_weights.pt`  
- Updated embeddings file (e.g., `clip_embeddings_lora.npy`)

###  3. `main.py` *(optional)* extracted images and descriptions are already stored in zip file  
```bash
python main.py --input_csv aml_image_metadata.csv --output_csv descriptions.csv
```
You can set:
- `--mode` = `zero-shot`, `lora`, or `gpt`
- `--limit` = number of samples

---

##  Outputs (Generated at Runtime)

The following files will be generated:
| File | Description |
|------|-------------|
| `gpt_descriptions.csv` | Descriptions from all 3 generation modes |
| `clip_embeddings.npy` | CLIP image embeddings |
| `clip_embeddings_lora.npy` | LoRA-adapted embeddings |
| `evaluation_metrics.json` | BLEU, ROUGE, SBERT, and CLIP similarity |
| `lora_weights.pt` | LoRA fine-tuned weights |

---

##  Evaluation

Each generation method is evaluated using:
- BLEU / ROUGE (linguistic similarity)
- CLIP similarity (multimodal alignment)
- Sentence-BERT (semantic similarity)
- Retrieval accuracy and confusion matrices

---

##  Example Output

**Input class:** Myeloblast  
**Generated (GPT):**
> “The cell is large with a round nucleus and a high nuclear-to-cytoplasmic ratio. Fine chromatin and visible nucleoli are present. The cytoplasm is lightly basophilic.”

---

##  References

- CLIP (OpenAI)
- GPT-3.5 (OpenAI API)
- PEFT / LoRA (HuggingFace)
- Mindray Blood Cell Atlas
- Dataset: AML-Cytomorphology_LMU: https://www.cancerimagingarchive.net/collection/aml-cytomorphology_lmu/

---

For questions or feedback, contact [pooja.chhaya.21@ucl.ac.uk].
