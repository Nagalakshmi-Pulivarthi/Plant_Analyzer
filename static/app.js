// Plant common names lookup - maps scientific names to common names
const plantCommonNames = {
    'epipremnum aureum': 'Pothos',
    'epipremnum pinnatum': 'Pothos',
    'scindapsus aureus': 'Pothos',
    'monstera deliciosa': 'Swiss Cheese Plant',
    'ficus lyrata': 'Fiddle Leaf Fig',
    'ficus benjamina': 'Weeping Fig',
    'ficus elastica': 'Rubber Plant',
    'spathiphyllum': 'Peace Lily',
    'spathiphyllum wallisii': 'Peace Lily',
    'dracaena marginata': 'Dragon Tree',
    'dracaena fragrans': 'Corn Plant',
    'sansevieria trifasciata': 'Snake Plant',
    'sansevieria': 'Snake Plant',
    'chlorophytum comosum': 'Spider Plant',
    'pothos': 'Pothos',
    'philodendron': 'Philodendron',
    'philodendron hederaceum': 'Heartleaf Philodendron',
    'alocasia': 'Elephant Ear',
    'alocasia amazonica': 'Elephant Ear',
    'calathea': 'Calathea',
    'maranta leuconeura': 'Prayer Plant',
    'zamioculcas zamiifolia': 'ZZ Plant',
    'crassula ovata': 'Jade Plant',
    'echeveria': 'Echeveria',
    'kalanchoe': 'Kalanchoe',
    'senecio rowleyanus': 'String of Pearls',
    'tradescantia': 'Spiderwort',
    'tradescantia zebrina': 'Wandering Jew',
    'peperomia': 'Peperomia',
    'hoya': 'Wax Plant',
    'hoya carnosa': 'Wax Plant',
    'senecio': 'Senecio',
    'begonia': 'Begonia',
    'anthurium': 'Anthurium',
    'dieffenbachia': 'Dumb Cane',
    'aglaonema': 'Chinese Evergreen',
    'syngonium podophyllum': 'Arrowhead Plant',
    'schefflera': 'Umbrella Tree',
    'asparagus fern': 'Asparagus Fern',
    'asparagus setaceus': 'Asparagus Fern',
    'pilea peperomioides': 'Chinese Money Plant',
    'oxalis triangularis': 'Purple Shamrock',
    'strelitzia reginae': 'Bird of Paradise',
    'yucca': 'Yucca',
    'cordyline': 'Ti Plant',
    'croton': 'Croton',
    'codiaeum variegatum': 'Croton',
    'hibiscus': 'Hibiscus',
    'bougainvillea': 'Bougainvillea',
    'rose': 'Rose',
    'rosa': 'Rose',
    'lavender': 'Lavender',
    'lavandula': 'Lavender',
    'basil': 'Basil',
    'ocimum basilicum': 'Basil',
    'mint': 'Mint',
    'mentha': 'Mint',
    'rosemary': 'Rosemary',
    'rosmarinus officinalis': 'Rosemary',
    'tomato': 'Tomato',
    'solanum lycopersicum': 'Tomato',
    'pepper': 'Pepper',
    'capsicum': 'Pepper',
    'fern': 'Fern',
    'nephrolepis': 'Boston Fern',
    'asplenium nidus': 'Bird\'s Nest Fern',
    'adiantum': 'Maidenhair Fern',
    'pteris': 'Brake Fern',
    'cactus': 'Cactus',
    'opuntia': 'Prickly Pear',
    'echinocactus': 'Barrel Cactus',
    'mammillaria': 'Pincushion Cactus',
    'succulent': 'Succulent'
};

// Function to get common name from scientific name
function getCommonName(scientificName) {
    if (!scientificName) return null;
    const normalized = scientificName.toLowerCase().trim();
    // Direct lookup
    if (plantCommonNames[normalized]) {
        return plantCommonNames[normalized];
    }
    // Try partial match (e.g., "Epipremnum aureum" matches "epipremnum aureum")
    for (const [sciName, commonName] of Object.entries(plantCommonNames)) {
        if (normalized.includes(sciName) || sciName.includes(normalized)) {
            return commonName;
        }
    }
    // Try matching by first word (genus)
    const firstWord = normalized.split(' ')[0];
    for (const [sciName, commonName] of Object.entries(plantCommonNames)) {
        if (sciName.startsWith(firstWord)) {
            return commonName;
        }
    }
    return null;
}

// DOM elements
const fileInput = document.getElementById('fileInput');
const imagePlaceholder = document.getElementById('imagePlaceholder');
const imagePreview = document.getElementById('imagePreview');
const previewImage = document.getElementById('previewImage');
const loadingIndicator = document.getElementById('loadingIndicator');
const errorMessage = document.getElementById('errorMessage');
const skeletonScreen = document.getElementById('skeletonScreen');

// Section elements for showing/hiding
const rightContent = document.getElementById('rightContent');
const problemSection = document.getElementById('problemSection');
const recommendationsSection = document.getElementById('recommendationsSection');
const severitySection = document.getElementById('severitySection');
const bottomSection = document.getElementById('bottomSection');
const summarySection = document.getElementById('summarySection');

// Plant analysis fields
const plantName = document.getElementById('plantName');
const categoryFamily = document.getElementById('categoryFamily');
const suitability = document.getElementById('suitability');
const healthStatus = document.getElementById('healthStatus');
const healthStatusBadge = document.getElementById('healthStatusBadge');
const problemDescription = document.getElementById('problemDescription');
const recommendationsGrid = document.getElementById('recommendationsGrid');
const summaryBox = document.getElementById('summaryBox');

// Confidence warning elements
const confidenceWarning = document.getElementById('confidenceWarning');
const confidenceWarningDetail = document.getElementById('confidenceWarningDetail');
const confidenceBadge = document.getElementById('confidenceBadge');

// Severity assessment fields
const severityScore = document.getElementById('severityScore');
const severityLabel = document.getElementById('severityLabel');
const severityPrognosis = document.getElementById('severityPrognosis');
const priorityActionsList = document.getElementById('priorityActionsList');
const recoveryTimeline = document.getElementById('recoveryTimeline');

// Additional observation fields (new format)
const bacteriaFungus = document.getElementById('bacteriaFungus');
const nutrientDeficiency = document.getElementById('nutrientDeficiency');
const pestDamage = document.getElementById('pestDamage');
const waterSunlightStress = document.getElementById('waterSunlightStress');
const damageType = document.getElementById('damageType');

// Make the preview image clickable to upload a new image
if (previewImage) {
    previewImage.addEventListener('click', () => {
        fileInput.click();
    });
}

fileInput.addEventListener('change', (e) => {
    handleFile(e.target.files[0]);
});

// Drag and drop on image placeholder
imagePlaceholder.addEventListener('dragover', (e) => {
    e.preventDefault();
    imagePlaceholder.classList.add('drag-over');
});

imagePlaceholder.addEventListener('dragleave', () => {
    imagePlaceholder.classList.remove('drag-over');
});

imagePlaceholder.addEventListener('drop', (e) => {
    e.preventDefault();
    imagePlaceholder.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file) {
        fileInput.files = e.dataTransfer.files;
        handleFile(file);
    }
});

imagePlaceholder.addEventListener('click', () => {
    fileInput.click();
});

// Keyboard navigation for image placeholder
imagePlaceholder.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        fileInput.click();
    }
});

function handleFile(file) {
    if (!file) return;
    
    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
        showError('Invalid file type. Please upload a JPG, PNG, or WEBP image.');
        return;
    }
    
    // Validate file size (10MB)
    const maxSize = 10 * 1024 * 1024; // 10MB in bytes
    if (file.size > maxSize) {
        showError('File too large. Maximum size is 10MB.');
        return;
    }
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        if (previewImage && imagePreview) {
            // Set up image load handler to ensure it displays
            previewImage.onload = () => {
                imagePlaceholder.style.display = 'none';
                imagePreview.style.display = 'flex';
                previewImage.style.display = 'block';
            };
            previewImage.onerror = () => {
                showError('Error loading image preview. Please try again.');
            };
            previewImage.src = e.target.result;
            hideError();
            // Don't call hideResults() here - it will be called by analyzePlant if needed
            // Plant details section will be shown in displayResults when data is available
        }
    };
    reader.onerror = () => {
        showError('Error reading file. Please try again.');
    };
    reader.readAsDataURL(file);
}

// Analyze on image upload (auto-analyze)
fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (file) {
        // Wait a bit for preview to show, then analyze
        setTimeout(async () => {
            await analyzePlant(file);
        }, 500);
    }
});

async function analyzePlant(file) {
    // Show loading, hide results and errors
    showLoading();
    hideError();
    hideResults();
    showSkeleton();
    
    try {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        const results = await response.json();
        // Small delay for smooth transition
        setTimeout(() => {
            hideSkeleton();
            displayResults(results);
        }, 200);
        
    } catch (error) {
        hideSkeleton();
        showError(`Error analyzing plant: ${error.message}`);
    } finally {
        hideLoading();
    }
}

function displayResults(results) {
    // Reset opacity
    rightContent.style.opacity = '1';
    
    // Display plant observations - only show if there's meaningful data
    // Support both old format (nested) and new format (flat)
    const obs = results.plant_observations || {};
    const hasPlantData = obs && (
        (obs.plant_name && obs.plant_name !== 'Unknown' && obs.plant_name !== '') ||
        (obs.plant_identification && obs.plant_identification.plant_name && obs.plant_identification.plant_name !== 'Unknown') ||
        (obs.plant_family && obs.plant_family !== '' && obs.plant_family !== '-') ||
        (obs.category_family && obs.category_family.category_or_family && obs.category_family.category_or_family !== '-') ||
        (obs.indoor_or_outdoor && obs.indoor_or_outdoor !== '' && obs.indoor_or_outdoor !== '-') ||
        (obs.suitability && obs.suitability.indoor_outdoor && obs.suitability.indoor_outdoor !== '-')
    );
    
    // Show plant details section only when there's data
    if (hasPlantData) {
        rightContent.style.display = 'flex';
        
        // Plant Name - Support both new format (direct) and old format (nested)
        const plantNameValue = obs.plant_name || (obs.plant_identification && obs.plant_identification.plant_name) || 'Unknown';
        if (plantNameValue !== 'Unknown' && plantNameValue !== '-') {
            let scientificName = null;
            let commonName = null;
            
            // Check if it already contains parentheses (common format: "Common Name (Scientific Name)" or "Scientific Name (Common Name)")
            if (plantNameValue.includes('(') && plantNameValue.includes(')')) {
                const match = plantNameValue.match(/^(.+?)\s*\((.+?)\)$/);
                if (match) {
                    const part1 = match[1].trim();
                    const part2 = match[2].trim();
                    // Check which part is scientific name (two words, both start with capital)
                    const part1IsScientific = /^[A-Z][a-z]+\s+[A-Z][a-z]+/.test(part1);
                    const part2IsScientific = /^[A-Z][a-z]+\s+[A-Z][a-z]+/.test(part2);
                    
                    if (part1IsScientific && !part2IsScientific) {
                        // Format: "Scientific Name (Common Name)"
                        scientificName = part1;
                        commonName = part2;
                    } else if (part2IsScientific && !part1IsScientific) {
                        // Format: "Common Name (Scientific Name)"
                        scientificName = part2;
                        commonName = part1;
                    } else {
                        // Unclear format, assume first is common, second is scientific
                        scientificName = part2;
                        commonName = part1;
                    }
                }
            } else if (plantNameValue.includes(',')) {
                // Format: "Common Name, Scientific Name" or "Scientific Name, Common Name"
                const parts = plantNameValue.split(',').map(p => p.trim());
                if (parts.length >= 2) {
                    const part1IsScientific = /^[A-Z][a-z]+\s+[A-Z][a-z]+/.test(parts[0]);
                    const part2IsScientific = /^[A-Z][a-z]+\s+[A-Z][a-z]+/.test(parts[1]);
                    
                    if (part1IsScientific && !part2IsScientific) {
                        scientificName = parts[0];
                        commonName = parts[1];
                    } else if (part2IsScientific && !part1IsScientific) {
                        scientificName = parts[1];
                        commonName = parts[0];
                    } else {
                        scientificName = parts[1];
                        commonName = parts[0];
                    }
                }
            } else {
                // Check if it's a scientific name (two words, both start with capital)
                const words = plantNameValue.split(/\s+/);
                if (words.length >= 2 && /^[A-Z][a-z]+/.test(words[0]) && /^[A-Z][a-z]+/.test(words[1])) {
                    // Likely scientific name only - try to find common name
                    scientificName = plantNameValue;
                    commonName = getCommonName(plantNameValue);
                } else {
                    // Likely common name only - try to find scientific name by reverse lookup
                    commonName = plantNameValue;
                    // Try to find scientific name from common name (reverse lookup)
                    for (const [sciName, commName] of Object.entries(plantCommonNames)) {
                        if (commName.toLowerCase() === plantNameValue.toLowerCase()) {
                            scientificName = sciName.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                            break;
                        }
                    }
                }
            }
            
            // Always try to find both names if we have at least one
            if (scientificName && !commonName) {
                commonName = getCommonName(scientificName);
            }
            
            // If we only have a common name, try to find scientific name by reverse lookup
            if (commonName && !scientificName) {
                // Try to find scientific name from common name (reverse lookup)
                for (const [sciName, commName] of Object.entries(plantCommonNames)) {
                    if (commName.toLowerCase() === commonName.toLowerCase()) {
                        scientificName = sciName.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                        break;
                    }
                }
            }
            
            // Format the display: Always show both names if available
            let displayName;
            if (scientificName && commonName) {
                // Display: "Scientific Name (Common Name)" - both names shown
                displayName = `${scientificName} <span class="common-name">(${commonName})</span>`;
            } else if (scientificName) {
                // Only scientific name available - try one more time to find common name
                const foundCommonName = getCommonName(scientificName);
                if (foundCommonName) {
                    displayName = `${scientificName} <span class="common-name">(${foundCommonName})</span>`;
                } else {
                    // Show scientific name only if we can't find common name
                    displayName = scientificName;
                }
            } else if (commonName) {
                // Only common name available - try one more time to find scientific name
                for (const [sciName, commName] of Object.entries(plantCommonNames)) {
                    if (commName.toLowerCase() === commonName.toLowerCase()) {
                        const foundScientificName = sciName.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
                        displayName = `${foundScientificName} <span class="common-name">(${commonName})</span>`;
                        break;
                    }
                }
                if (!displayName) {
                    // Show common name only if we can't find scientific name
                    displayName = commonName;
                }
            } else {
                // Fallback to original value
                displayName = plantNameValue;
            }
            
            plantName.innerHTML = displayName;
            plantName.classList.remove('empty-state');
        } else {
            plantName.textContent = 'Not detected';
            plantName.classList.add('empty-state');
        }
    
    // Category/Family - Support both new format (direct) and old format (nested)
        const categoryValue = obs.plant_family || (obs.category_family && obs.category_family.category_or_family) || '-';
        if (categoryValue !== '-' && categoryValue !== '' && categoryValue) {
            categoryFamily.textContent = categoryValue;
            categoryFamily.classList.remove('empty-state');
        } else {
            categoryFamily.textContent = 'No data available';
            categoryFamily.classList.add('empty-state');
        }
    
    // Suitability - Support both new format (direct) and old format (nested)
        const suitabilityValue = obs.indoor_or_outdoor || (obs.suitability && obs.suitability.indoor_outdoor) || '-';
        if (suitabilityValue !== '-' && suitabilityValue !== '' && suitabilityValue) {
            suitability.textContent = suitabilityValue;
            suitability.classList.remove('empty-state');
        } else {
            suitability.textContent = 'No data available';
            suitability.classList.add('empty-state');
        }
    
    // Health Status - Support both new format (direct) and old format (nested)
        let healthValue = '-';
        if (typeof obs.leaf_health === 'string') {
            // New format: direct string value
            healthValue = obs.leaf_health;
        } else if (obs.leaf_health && typeof obs.leaf_health === 'object' && obs.leaf_health.issues) {
            // Old format: nested object with issues property
            healthValue = obs.leaf_health.issues;
        }
        healthStatus.textContent = healthValue !== '-' && healthValue !== '' ? healthValue : 'Not analyzed';
        healthStatus.classList.toggle('empty-state', healthValue === '-' || healthValue === '');
        
        // Add health status badge — use analysis_path for reliable classification
        updateHealthStatusBadge(healthValue, results.analysis_path);
        
        // Display additional observation fields if available (new format)
        displayAdditionalObservations(obs);
        
        // Update grid layout
        const mainContent = rightContent.closest('.main-content');
        if (mainContent) {
            mainContent.classList.remove('single-column');
        }
    } else {
        // No data - hide plant details section
        rightContent.style.display = 'none';
        // Update grid layout to single column if no data
        const mainContent = rightContent.closest('.main-content');
        if (mainContent) {
            mainContent.classList.add('single-column');
        }
    }
    
    // Display confidence warning
    // Remove any existing confidence badge first to prevent stacking
    const existingBadge = document.getElementById('inlinConfidenceBadge');
    if (existingBadge) existingBadge.remove();

    const confidence = obs.identification_confidence;
    if (confidence !== undefined && confidence !== null) {
        if (confidence >= 80) {
            confidenceWarning.style.display = 'none';
            plantName.insertAdjacentHTML('afterend',
                `<span id="inlinConfidenceBadge" class="confidence-badge confidence-high" style="margin-left:10px;">✓ ${confidence}% confident</span>`
            );
        } else if (confidence >= 60) {
            confidenceWarning.style.display = 'none';
            plantName.insertAdjacentHTML('afterend',
                `<span id="inlinConfidenceBadge" class="confidence-badge confidence-medium" style="margin-left:10px;">~ ${confidence}% confident</span>`
            );
        } else {
            // Low confidence — show warning banner only, no inline badge
            confidenceWarningDetail.textContent =
                `Confidence is only ${confidence}%. This may be due to image angle, poor lighting, heavy damage, or an uncommon species. ` +
                `Try uploading a clearer, closer photo of a single leaf for better results.`;
            confidenceWarning.style.display = 'flex';
        }
    } else {
        confidenceWarning.style.display = 'none';
    }

    // Display problem description - always show
    const hasProblem = results.recommendations && results.recommendations.ProblemDescription && 
                       results.recommendations.ProblemDescription.trim() !== '';
    if (hasProblem) {
        problemDescription.innerHTML = `<p>${escapeHtml(results.recommendations.ProblemDescription)}</p>`;
    } else {
        problemDescription.innerHTML = '<span class="placeholder-text empty-state">No problems detected</span>';
    }
    problemSection.style.display = 'flex';
    
    // Display recommendations - only show if there are recommendations
    const hasRecommendations = results.recommendations && results.recommendations.Recommendations && 
                               results.recommendations.Recommendations.length > 0;
    if (hasRecommendations) {
        const recs = results.recommendations.Recommendations;
        recommendationsGrid.innerHTML = '';

        // Change heading based on analysis path
        const recHeading = document.querySelector('#recommendationsSection .section-heading');
        if (recHeading) {
            recHeading.textContent = results.analysis_path === 'healthy' ? 'Care Tips' : 'Recommendations';
        }

        // Use 3 columns if more than 4 recommendations
        if (recs.length > 4) {
            recommendationsGrid.classList.add('three-columns');
        } else {
            recommendationsGrid.classList.remove('three-columns');
        }
        
        const isHealthy = results.analysis_path === 'healthy';

        recs.forEach((rec, index) => {
            const recDiv = document.createElement('div');
            recDiv.className = isHealthy
                ? 'recommendation-placeholder rec-care'
                : 'recommendation-placeholder rec-action';
            const heading = rec.Heading || 'Recommendation';
            const icon = getRecommendationIcon(heading);
            recDiv.style.animationDelay = `${index * 0.1}s`;
            recDiv.innerHTML = `
                <div style="text-align: left; width: 100%;">
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                        <span style="font-size: 24px;">${icon}</span>
                        <strong style="color: #1e293b; font-size: 16px; font-weight: 600;">${escapeHtml(heading)}</strong>
                    </div>
                    <p style="margin-top: 0; color: #475569; font-size: 14px; line-height: 1.6;">${escapeHtml(rec.Description || '')}</p>
                </div>
            `;
            recommendationsGrid.appendChild(recDiv);
        });
        
        recommendationsSection.style.display = 'block';
    } else {
        recommendationsSection.style.display = 'none';
    }
    
    // Display severity assessment — only show when plant has issues (not healthy path)
    const hasSeverity = results.severity_assessment && results.analysis_path !== 'healthy';
    if (hasSeverity) {
        const sa = results.severity_assessment;

        // Score with color coding
        const score = sa.severity_score || '-';
        severityScore.textContent = score;
        severityScore.className = 'severity-score-number';
        if (score >= 7) severityScore.classList.add('severity-critical');
        else if (score >= 5) severityScore.classList.add('severity-high');
        else if (score >= 3) severityScore.classList.add('severity-moderate');
        else severityScore.classList.add('severity-low');

        severityLabel.textContent = sa.severity_label || '-';
        severityPrognosis.textContent = sa.prognosis || '-';

        // Priority actions list
        priorityActionsList.innerHTML = '';
        if (sa.priority_actions && sa.priority_actions.length > 0) {
            sa.priority_actions.forEach(action => {
                const li = document.createElement('li');
                li.textContent = action;
                priorityActionsList.appendChild(li);
            });
        }

        recoveryTimeline.textContent = sa.recovery_timeline || '-';
        severitySection.style.display = 'block';
    } else {
        severitySection.style.display = 'none';
    }

    // Display summary
    const hasSummary = results.recommendations && results.recommendations.FinalSummary &&
                       results.recommendations.FinalSummary.trim() !== '';
    if (hasSummary) {
        summaryBox.innerHTML = `<p>${escapeHtml(results.recommendations.FinalSummary)}</p>`;
        summarySection.style.display = 'flex';
        bottomSection.style.display = 'block';
        const summaryContainer = document.getElementById('summaryContainer');
        if (summaryContainer) summaryContainer.style.display = 'flex';
    } else {
        summarySection.style.display = 'none';
        bottomSection.style.display = 'none';
    }
}

function displayAdditionalObservations(obs) {
    // Display additional observation fields from new format
    // Only show fields that have meaningful data
    
    // Bacteria or Fungus Detected
    const bacteriaValue = obs.bacteria_or_fungus_detected;
    if (bacteriaFungus) {
        if (bacteriaValue && bacteriaValue !== '' && bacteriaValue !== 'None' && bacteriaValue !== '-') {
            bacteriaFungus.textContent = bacteriaValue;
            bacteriaFungus.classList.remove('empty-state');
            bacteriaFungus.parentElement.parentElement.style.display = 'flex';
        } else {
            bacteriaFungus.textContent = 'None detected';
            bacteriaFungus.classList.add('empty-state');
            // Only hide if all additional fields are empty
        }
    }
    
    // Nutrient Deficiency Signs
    const nutrientValue = obs.nutrient_deficiency_signs;
    if (nutrientDeficiency) {
        if (nutrientValue && nutrientValue !== '' && nutrientValue !== 'None' && nutrientValue !== '-' && nutrientValue.toLowerCase() !== 'unknown') {
            nutrientDeficiency.textContent = nutrientValue;
            nutrientDeficiency.classList.remove('empty-state');
            nutrientDeficiency.parentElement.parentElement.style.display = 'flex';
        } else {
            nutrientDeficiency.textContent = 'No signs detected';
            nutrientDeficiency.classList.add('empty-state');
        }
    }
    
    // Pest Damage
    const pestValue = obs.pest_damage;
    if (pestDamage) {
        if (pestValue && pestValue !== '' && pestValue !== 'None' && pestValue !== '-' && pestValue.toLowerCase() !== 'unknown') {
            pestDamage.textContent = pestValue;
            pestDamage.classList.remove('empty-state');
            pestDamage.parentElement.parentElement.style.display = 'flex';
        } else {
            pestDamage.textContent = 'No damage detected';
            pestDamage.classList.add('empty-state');
        }
    }
    
    // Water or Sunlight Stress
    const stressValue = obs.water_or_sunlight_stress;
    if (waterSunlightStress) {
        if (stressValue && stressValue !== '' && stressValue !== 'None' && stressValue !== '-' && stressValue.toLowerCase() !== 'unknown') {
            waterSunlightStress.textContent = stressValue;
            waterSunlightStress.classList.remove('empty-state');
            waterSunlightStress.parentElement.parentElement.style.display = 'flex';
        } else {
            waterSunlightStress.textContent = 'No stress detected';
            waterSunlightStress.classList.add('empty-state');
        }
    }
    
    // Damage Type
    const damageValue = obs.damage_type;
    if (damageType) {
        if (damageValue && damageValue !== '' && damageValue !== 'None' && damageValue !== '-' && damageValue.toLowerCase() !== 'unknown') {
            damageType.textContent = damageValue;
            damageType.classList.remove('empty-state');
            damageType.parentElement.parentElement.style.display = 'flex';
        } else {
            damageType.textContent = 'No damage detected';
            damageType.classList.add('empty-state');
        }
    }
}

function updateHealthStatusBadge(healthValue, analysisPath) {
    if (!healthValue || healthValue === '-' || healthValue === 'Not analyzed') {
        healthStatusBadge.style.display = 'none';
        return;
    }

    healthStatusBadge.style.display = 'inline-flex';
    healthStatusBadge.className = 'health-status-badge';

    // Use analysis_path from the graph for reliable classification
    // This avoids keyword-matching bugs on complex health descriptions
    if (analysisPath === 'healthy') {
        healthStatusBadge.classList.add('healthy');
        healthStatusBadge.textContent = '✓ Healthy';
    } else if (analysisPath === 'viral') {
        healthStatusBadge.classList.add('unhealthy');
        healthStatusBadge.textContent = '✗ Viral Infection';
    } else if (analysisPath === 'fungal_bacterial') {
        healthStatusBadge.classList.add('unhealthy');
        healthStatusBadge.textContent = '✗ Infection Detected';
    } else if (analysisPath === 'pest') {
        healthStatusBadge.classList.add('warning');
        healthStatusBadge.textContent = '⚠ Pest Damage';
    } else if (analysisPath === 'stress') {
        healthStatusBadge.classList.add('warning');
        healthStatusBadge.textContent = '⚠ Stress Detected';
    } else {
        // Fallback: use health text if analysis_path not available
        const healthLower = healthValue.toLowerCase();
        if (healthLower.includes('healthy') || healthLower.includes('good')) {
            healthStatusBadge.classList.add('healthy');
            healthStatusBadge.textContent = '✓ Healthy';
        } else {
            healthStatusBadge.classList.add('warning');
            healthStatusBadge.textContent = '⚠ Needs Attention';
        }
    }
}

function getRecommendationIcon(heading) {
    if (!heading) return '🌱';
    
    const headingLower = heading.toLowerCase();
    
    // Watering related
    if (headingLower.includes('water') || headingLower.includes('watering') || headingLower.includes('moisture')) {
        return '💧';
    }
    // Sunlight related
    if (headingLower.includes('sun') || headingLower.includes('light') || headingLower.includes('sunlight') || headingLower.includes('bright')) {
        return '☀️';
    }
    // Fertilizing related
    if (headingLower.includes('fertiliz') || headingLower.includes('nutrient') || headingLower.includes('feed')) {
        return '🌿';
    }
    // Temperature related
    if (headingLower.includes('temperat') || headingLower.includes('warm') || headingLower.includes('cold') || headingLower.includes('climate')) {
        return '🌡️';
    }
    // Humidity related
    if (headingLower.includes('humidity') || headingLower.includes('moist') || headingLower.includes('air')) {
        return '💨';
    }
    // Soil related
    if (headingLower.includes('soil') || headingLower.includes('potting') || headingLower.includes('drainage')) {
        return '🪴';
    }
    // Pruning related
    if (headingLower.includes('prun') || headingLower.includes('trim') || headingLower.includes('cut')) {
        return '✂️';
    }
    // Pests/Disease related
    if (headingLower.includes('pest') || headingLower.includes('disease') || headingLower.includes('insect') || headingLower.includes('bug')) {
        return '🐛';
    }
    // Repotting related
    if (headingLower.includes('repot') || headingLower.includes('transplant') || headingLower.includes('pot')) {
        return '🔄';
    }
    
    // Default icon
    return '🌱';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showLoading() {
    loadingIndicator.style.display = 'flex';
}

function hideLoading() {
    loadingIndicator.style.display = 'none';
}

function showSkeleton() {
    if (skeletonScreen) {
        skeletonScreen.style.display = 'flex';
        rightContent.style.opacity = '0.5';
    }
}

function hideSkeleton() {
    if (skeletonScreen) {
        skeletonScreen.style.display = 'none';
        rightContent.style.opacity = '1';
    }
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}

function hideError() {
    errorMessage.style.display = 'none';
}

function hideResults() {
    // Reset all fields to placeholder state
    plantName.textContent = 'Not detected';
    plantName.classList.add('empty-state');
    categoryFamily.textContent = 'No data available';
    categoryFamily.classList.add('empty-state');
    suitability.textContent = 'No data available';
    suitability.classList.add('empty-state');
    healthStatus.textContent = 'Not analyzed';
    healthStatus.classList.add('empty-state');
    healthStatusBadge.style.display = 'none';
    
    // Reset additional observation fields
    if (bacteriaFungus) {
        bacteriaFungus.textContent = 'None detected';
        bacteriaFungus.classList.add('empty-state');
    }
    if (nutrientDeficiency) {
        nutrientDeficiency.textContent = 'No signs detected';
        nutrientDeficiency.classList.add('empty-state');
    }
    if (pestDamage) {
        pestDamage.textContent = 'No damage detected';
        pestDamage.classList.add('empty-state');
    }
    if (waterSunlightStress) {
        waterSunlightStress.textContent = 'No stress detected';
        waterSunlightStress.classList.add('empty-state');
    }
    if (damageType) {
        damageType.textContent = 'No damage detected';
        damageType.classList.add('empty-state');
    }
    
    // Hide plant details section when there's no data
    rightContent.style.display = 'none';
    
    // Hide other sections
    confidenceWarning.style.display = 'none';
    const prevBadge = document.getElementById('inlinConfidenceBadge');
    if (prevBadge) prevBadge.remove();
    problemDescription.innerHTML = '<span class="placeholder-text empty-state">No problems detected</span>';
    recommendationsSection.style.display = 'none';
    severitySection.style.display = 'none';
    bottomSection.style.display = 'none';
    summarySection.style.display = 'none';
    
    // Reset summary container
    const summaryContainer = document.getElementById('summaryContainer');
    if (summaryContainer) {
        summaryContainer.style.display = 'flex';
    }
    
    // Update grid layout to single column when no data
    const mainContent = rightContent.closest('.main-content');
    if (mainContent) {
        mainContent.classList.add('single-column');
    }
    
    // Clear content
    problemDescription.innerHTML = '<span class="placeholder-text empty-state">No problems detected</span>';
    recommendationsGrid.innerHTML = '';
    priorityActionsList.innerHTML = '';
    summaryBox.innerHTML = '<span class="placeholder-text empty-state">No summary available</span>';
    
    // Don't reset image view here - keep the uploaded image visible during analysis
    // Only reset when explicitly needed (e.g., when starting a new upload)
}
