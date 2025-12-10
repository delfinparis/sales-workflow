/**
 * Rea's Newly Licensed Leads Import Script
 *
 * This Google Apps Script:
 * 1. Adds a custom menu to Google Sheets
 * 2. Filters leads by Chicago-area zipcodes
 * 3. Filters by approved license types (Broker exams only)
 * 4. Deduplicates by email
 * 5. Sends cleaned data to Make.com webhook → Monday.com
 *
 * SETUP:
 * 1. Open your Google Sheet with AMP passer data
 * 2. Go to Extensions → Apps Script
 * 3. Delete any existing code and paste this entire script
 * 4. Update MAKE_WEBHOOK_URL with your actual webhook URL
 * 5. Save and refresh the sheet
 * 6. You'll see a new "Rea Import" menu
 */

// ============================================
// CONFIGURATION - UPDATE THESE VALUES
// ============================================

const MAKE_WEBHOOK_URL = 'YOUR_MAKE_WEBHOOK_URL_HERE';  // Get this from Make.com

// Column names in the CSV (case-sensitive, must match exactly)
const COLUMNS = {
  FIRST_NAME: 'First Name',
  LAST_NAME: 'Last Name',
  CITY: 'City',
  PHONE: 'Phone',
  EMAIL: 'Email',
  TEST_DATE: 'Test Date',
  PORTION: 'Portion'  // License type column
};

// Approved license types (leads with these values in "Portion" column will be INCLUDED)
const APPROVED_LICENSE_TYPES = [
  'IL Broker National Portion',
  'IL Broker State Portion',
  'IL Broker Reciprocity Examination'
];

// Chicago-area zipcodes (leads with these zipcodes will be INCLUDED)
// Note: The CSV has "City" not "Zip" - we'll need to handle this
const CHICAGO_AREA_ZIPCODES = [
  // Core Chicago
  '60601', '60602', '60603', '60604', '60605', '60606', '60607', '60608', '60609',
  '60610', '60611', '60612', '60613', '60614', '60615', '60616', '60617', '60618',
  '60619', '60620', '60621', '60622', '60623', '60624', '60625', '60626', '60628',
  '60629', '60630', '60631', '60632', '60633', '60634', '60636', '60637', '60638',
  '60639', '60640', '60641', '60642', '60643', '60644', '60645', '60646', '60647',
  '60649', '60651', '60652', '60653', '60654', '60655', '60656', '60657', '60659',
  '60660', '60661',
  // North Suburbs
  '60007', '60013', '60018', '60025', '60030', '60031', '60032', '60033', '60034',
  '60035', '60036', '60037', '60038', '60039', '60040', '60041', '60042', '60043',
  '60044', '60045', '60046', '60047', '60048', '60049', '60050', '60051', '60052',
  '60053', '60054', '60055', '60056', '60057', '60058', '60059', '60060', '60061',
  '60062', '60063', '60064', '60065', '60066', '60067', '60068', '60069',
  '60002', '60010', '60011', '60015', '60020', '60073', '60075', '60079', '60083',
  '60084', '60085', '60087', '60088', '60089', '60092', '60096', '60099',
  '60001', '60012', '60014', '60021', '60071', '60072', '60080', '60081', '60097', '60098',
  // South Suburbs
  '60401', '60402', '60403', '60404', '60406', '60407', '60408', '60409', '60410',
  '60411', '60412', '60413', '60415', '60416', '60417', '60418', '60419', '60420',
  '60421', '60422', '60423', '60424', '60425', '60426', '60428', '60429', '60430',
  '60431', '60432', '60433', '60434', '60435', '60436', '60437', '60438', '60439',
  '60440', '60441', '60442', '60443', '60444', '60445', '60446', '60447', '60448',
  '60449', '60450', '60451', '60452', '60453', '60454', '60455', '60456', '60457',
  '60458', '60459', '60460', '60461', '60462', '60463', '60464', '60465', '60466',
  '60467', '60468', '60469', '60470', '60471', '60472', '60473', '60474', '60475',
  '60476', '60477', '60478', '60479', '60480', '60481', '60482', '60483', '60484',
  '60485', '60486', '60487', '60488', '60489', '60490', '60491', '60492',
  '60585', '60586', '60544', '60564', '60565',
  // West Suburbs
  '60501', '60502', '60503', '60504', '60505', '60506', '60507', '60508', '60509',
  '60510', '60511', '60512', '60513', '60514', '60515', '60516', '60517', '60518',
  '60519', '60520', '60521', '60522', '60523', '60524', '60525', '60526', '60527',
  '60528', '60529', '60530', '60532', '60536', '60537', '60538', '60539', '60540',
  '60541', '60542', '60543', '60545', '60548', '60554', '60555', '60559', '60560',
  '60561', '60563', '60566',
  // DuPage & Kane
  '60101', '60102', '60103', '60104', '60105', '60106', '60107', '60108', '60109',
  '60110', '60111', '60112', '60113', '60114', '60115', '60116', '60117', '60118',
  '60119', '60120', '60121', '60122', '60123', '60124', '60125', '60126', '60127',
  '60128', '60129', '60130', '60131', '60132', '60133', '60134', '60135', '60136',
  '60137', '60138', '60139', '60140', '60141', '60142', '60143', '60144', '60145',
  '60146', '60147', '60148', '60149', '60150', '60151', '60152', '60153', '60154',
  '60155', '60156', '60157', '60158', '60159', '60160', '60161', '60162', '60163',
  '60164', '60165', '60166', '60167', '60168', '60169', '60170', '60171', '60172',
  '60173', '60174', '60175', '60176', '60177', '60178', '60179', '60180', '60181',
  '60182', '60183', '60184', '60185', '60186', '60187', '60188', '60189', '60190',
  '60191', '60192', '60193', '60194', '60195', '60196', '60197', '60198', '60199'
];

// Chicago-area cities (since CSV has City, not Zip)
// This is a backup filter if zip isn't available
const CHICAGO_AREA_CITIES = [
  // Core Chicago
  'Chicago', 'CHICAGO',
  // North Shore
  'Evanston', 'Wilmette', 'Winnetka', 'Kenilworth', 'Glencoe', 'Highland Park',
  'Lake Forest', 'Lake Bluff', 'Highwood', 'Deerfield', 'Northbrook', 'Glenview',
  'Morton Grove', 'Niles', 'Skokie', 'Lincolnwood', 'Park Ridge', 'Des Plaines',
  // Northwest Suburbs
  'Arlington Heights', 'Mount Prospect', 'Prospect Heights', 'Wheeling', 'Buffalo Grove',
  'Palatine', 'Rolling Meadows', 'Schaumburg', 'Hoffman Estates', 'Streamwood',
  'Hanover Park', 'Bartlett', 'Elk Grove Village', 'Itasca', 'Roselle', 'Bloomingdale',
  // West Suburbs
  'Oak Park', 'River Forest', 'Forest Park', 'Maywood', 'Melrose Park', 'Elmwood Park',
  'Franklin Park', 'Northlake', 'Stone Park', 'Bellwood', 'Broadview', 'Westchester',
  'La Grange', 'La Grange Park', 'Western Springs', 'Hinsdale', 'Clarendon Hills',
  'Downers Grove', 'Woodridge', 'Lisle', 'Naperville', 'Aurora', 'Wheaton', 'Glen Ellyn',
  'Lombard', 'Villa Park', 'Addison', 'Elmhurst', 'Bensenville', 'Wood Dale',
  'Carol Stream', 'West Chicago', 'Warrenville', 'Winfield', 'Geneva', 'St Charles',
  'Batavia', 'North Aurora', 'Montgomery', 'Oswego', 'Plainfield', 'Bolingbrook',
  // South Suburbs
  'Oak Lawn', 'Evergreen Park', 'Beverly', 'Blue Island', 'Calumet City', 'Dolton',
  'Harvey', 'South Holland', 'Lansing', 'Munster', 'Hammond', 'East Chicago',
  'Gary', 'Merrillville', 'Schererville', 'Griffith', 'Highland', 'Tinley Park',
  'Orland Park', 'Palos Hills', 'Palos Heights', 'Worth', 'Chicago Ridge', 'Oak Forest',
  'Midlothian', 'Crestwood', 'Alsip', 'Burbank', 'Bridgeview', 'Justice', 'Hickory Hills',
  'Willow Springs', 'Lemont', 'Lockport', 'Homer Glen', 'New Lenox', 'Frankfort',
  'Mokena', 'Matteson', 'Richton Park', 'Park Forest', 'Olympia Fields', 'Flossmoor',
  'Homewood', 'Hazel Crest', 'Country Club Hills', 'Markham',
  // Southwest
  'Joliet', 'Romeoville', 'Crest Hill', 'Shorewood',
  // Lake County
  'Waukegan', 'North Chicago', 'Zion', 'Beach Park', 'Winthrop Harbor', 'Gurnee',
  'Libertyville', 'Mundelein', 'Vernon Hills', 'Lincolnshire', 'Long Grove',
  'Hawthorn Woods', 'Kildeer', 'Lake Zurich', 'Barrington', 'Barrington Hills',
  'Inverness', 'South Barrington', 'Deer Park', 'Fox Lake', 'Round Lake',
  'Grayslake', 'Lake Villa', 'Antioch', 'Wauconda', 'Island Lake',
  // McHenry County
  'Crystal Lake', 'McHenry', 'Woodstock', 'Cary', 'Algonquin', 'Lake in the Hills',
  'Huntley', 'Harvard', 'Marengo'
];

// ============================================
// MENU SETUP
// ============================================

function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Rea Import')
    .addItem('Preview Import (Dry Run)', 'previewImport')
    .addItem('Import to Monday', 'importToMonday')
    .addSeparator()
    .addItem('Show Statistics', 'showStatistics')
    .addToUi();
}

// ============================================
// MAIN FUNCTIONS
// ============================================

/**
 * Preview what will be imported without actually sending to Monday
 */
function previewImport() {
  const result = processLeads(true);

  const ui = SpreadsheetApp.getUi();
  ui.alert(
    'Preview Results',
    `Total rows in sheet: ${result.totalRows}\n` +
    `After license type filter: ${result.afterLicenseFilter}\n` +
    `After city filter: ${result.afterCityFilter}\n` +
    `After email deduplication: ${result.afterDedup}\n\n` +
    `READY TO IMPORT: ${result.readyToImport} leads\n\n` +
    `Excluded:\n` +
    `  - Wrong license type: ${result.excludedLicenseType}\n` +
    `  - Outside Chicago area: ${result.excludedCity}\n` +
    `  - Duplicate emails: ${result.excludedDuplicates}\n` +
    `  - Missing required data: ${result.excludedMissingData}`,
    ui.ButtonSet.OK
  );
}

/**
 * Show statistics about the current sheet
 */
function showStatistics() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  const headers = data[0];

  const licenseTypeCol = headers.indexOf(COLUMNS.PORTION);
  const cityCol = headers.indexOf(COLUMNS.CITY);

  // Count license types
  const licenseTypes = {};
  const cities = {};

  for (let i = 1; i < data.length; i++) {
    const licenseType = data[i][licenseTypeCol] || '(empty)';
    const city = data[i][cityCol] || '(empty)';

    licenseTypes[licenseType] = (licenseTypes[licenseType] || 0) + 1;
    cities[city] = (cities[city] || 0) + 1;
  }

  // Build report
  let report = `TOTAL ROWS: ${data.length - 1}\n\n`;

  report += 'LICENSE TYPES:\n';
  Object.keys(licenseTypes).sort().forEach(type => {
    const isApproved = APPROVED_LICENSE_TYPES.includes(type) ? ' ✓' : ' ✗';
    report += `  ${type}: ${licenseTypes[type]}${isApproved}\n`;
  });

  report += '\nTOP 20 CITIES:\n';
  const sortedCities = Object.entries(cities).sort((a, b) => b[1] - a[1]).slice(0, 20);
  sortedCities.forEach(([city, count]) => {
    const isChicago = CHICAGO_AREA_CITIES.some(c => c.toLowerCase() === city.toLowerCase()) ? ' ✓' : '';
    report += `  ${city}: ${count}${isChicago}\n`;
  });

  SpreadsheetApp.getUi().alert('Sheet Statistics', report, SpreadsheetApp.getUi().ButtonSet.OK);
}

/**
 * Process and import leads to Monday via Make webhook
 */
function importToMonday() {
  const ui = SpreadsheetApp.getUi();

  // Confirm before importing
  const response = ui.alert(
    'Confirm Import',
    'This will import filtered leads to Monday.com.\n\n' +
    'Are you sure you want to continue?',
    ui.ButtonSet.YES_NO
  );

  if (response !== ui.Button.YES) {
    return;
  }

  const result = processLeads(false);

  if (result.readyToImport === 0) {
    ui.alert(
      'No Leads to Import',
      'After filtering, there are no leads to import.\n\n' +
      `Excluded:\n` +
      `  - Wrong license type: ${result.excludedLicenseType}\n` +
      `  - Outside Chicago area: ${result.excludedCity}\n` +
      `  - Duplicate emails: ${result.excludedDuplicates}\n` +
      `  - Missing required data: ${result.excludedMissingData}`,
      ui.ButtonSet.OK
    );
    return;
  }

  // Send to Make webhook
  try {
    const payload = {
      leads: result.leads,
      importDate: new Date().toISOString(),
      source: 'AMP Passer List',
      stats: {
        total: result.totalRows,
        imported: result.readyToImport,
        excludedLicenseType: result.excludedLicenseType,
        excludedCity: result.excludedCity,
        excludedDuplicates: result.excludedDuplicates,
        excludedMissingData: result.excludedMissingData
      }
    };

    const options = {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    };

    const response = UrlFetchApp.fetch(MAKE_WEBHOOK_URL, options);
    const responseCode = response.getResponseCode();

    if (responseCode >= 200 && responseCode < 300) {
      ui.alert(
        'Import Successful!',
        `Successfully sent ${result.readyToImport} leads to Monday.com!\n\n` +
        `Summary:\n` +
        `  - Total rows: ${result.totalRows}\n` +
        `  - Imported: ${result.readyToImport}\n` +
        `  - Excluded (license type): ${result.excludedLicenseType}\n` +
        `  - Excluded (city): ${result.excludedCity}\n` +
        `  - Excluded (duplicates): ${result.excludedDuplicates}\n` +
        `  - Excluded (missing data): ${result.excludedMissingData}`,
        ui.ButtonSet.OK
      );
    } else {
      throw new Error(`HTTP ${responseCode}: ${response.getContentText()}`);
    }
  } catch (error) {
    ui.alert(
      'Import Failed',
      `Error sending to Make.com:\n\n${error.message}\n\n` +
      'Please check the webhook URL and try again.',
      ui.ButtonSet.OK
    );
  }
}

// ============================================
// HELPER FUNCTIONS
// ============================================

/**
 * Process leads with all filters
 * @param {boolean} dryRun - If true, don't actually send, just return stats
 * @returns {Object} Processing results and stats
 */
function processLeads(dryRun) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  const headers = data[0];

  // Get column indices
  const colIdx = {
    firstName: headers.indexOf(COLUMNS.FIRST_NAME),
    lastName: headers.indexOf(COLUMNS.LAST_NAME),
    city: headers.indexOf(COLUMNS.CITY),
    phone: headers.indexOf(COLUMNS.PHONE),
    email: headers.indexOf(COLUMNS.EMAIL),
    testDate: headers.indexOf(COLUMNS.TEST_DATE),
    portion: headers.indexOf(COLUMNS.PORTION)
  };

  // Validate required columns exist
  const missingCols = [];
  if (colIdx.firstName === -1) missingCols.push(COLUMNS.FIRST_NAME);
  if (colIdx.lastName === -1) missingCols.push(COLUMNS.LAST_NAME);
  if (colIdx.email === -1) missingCols.push(COLUMNS.EMAIL);
  if (colIdx.portion === -1) missingCols.push(COLUMNS.PORTION);

  if (missingCols.length > 0) {
    throw new Error(`Missing required columns: ${missingCols.join(', ')}`);
  }

  const stats = {
    totalRows: data.length - 1,  // Exclude header
    afterLicenseFilter: 0,
    afterCityFilter: 0,
    afterDedup: 0,
    readyToImport: 0,
    excludedLicenseType: 0,
    excludedCity: 0,
    excludedDuplicates: 0,
    excludedMissingData: 0,
    leads: []
  };

  const seenEmails = new Set();

  for (let i = 1; i < data.length; i++) {
    const row = data[i];

    const firstName = (row[colIdx.firstName] || '').toString().trim();
    const lastName = (row[colIdx.lastName] || '').toString().trim();
    const city = (row[colIdx.city] || '').toString().trim();
    const phone = (row[colIdx.phone] || '').toString().trim();
    const email = (row[colIdx.email] || '').toString().trim().toLowerCase();
    const testDate = row[colIdx.testDate];
    const portion = (row[colIdx.portion] || '').toString().trim();

    // Filter 1: License type
    if (!APPROVED_LICENSE_TYPES.includes(portion)) {
      stats.excludedLicenseType++;
      continue;
    }
    stats.afterLicenseFilter++;

    // Filter 2: Chicago area (by city name)
    const isChicagoArea = CHICAGO_AREA_CITIES.some(
      c => c.toLowerCase() === city.toLowerCase()
    );
    if (!isChicagoArea) {
      stats.excludedCity++;
      continue;
    }
    stats.afterCityFilter++;

    // Filter 3: Required data present
    if (!firstName || !lastName || !email) {
      stats.excludedMissingData++;
      continue;
    }

    // Filter 4: Dedupe by email
    if (seenEmails.has(email)) {
      stats.excludedDuplicates++;
      continue;
    }
    seenEmails.add(email);
    stats.afterDedup++;

    // Lead passed all filters
    stats.leads.push({
      firstName: firstName,
      lastName: lastName,
      email: email,
      phone: formatPhone(phone),
      city: city,
      testDate: testDate ? new Date(testDate).toISOString() : null,
      licenseType: portion,
      leadSource: 'AMP Passer List'
    });
  }

  stats.readyToImport = stats.leads.length;

  return stats;
}

/**
 * Format phone number to standard format
 */
function formatPhone(phone) {
  if (!phone) return '';

  // Remove all non-digits
  const digits = phone.toString().replace(/\D/g, '');

  // If 10 digits, format as (XXX) XXX-XXXX
  if (digits.length === 10) {
    return `(${digits.slice(0,3)}) ${digits.slice(3,6)}-${digits.slice(6)}`;
  }

  // If 11 digits starting with 1, format without country code
  if (digits.length === 11 && digits[0] === '1') {
    return `(${digits.slice(1,4)}) ${digits.slice(4,7)}-${digits.slice(7)}`;
  }

  // Return original if can't format
  return phone;
}
