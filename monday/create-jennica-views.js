/**
 * Create Jennica's Views - Monday.com API Script
 *
 * This script creates all 4 views for Jennica:
 * 1. 🟣 Jennica's Day (master daily view)
 * 2. Jennica - Today's Hunt ⭐
 * 3. Jennica - Timeout Returning Soon
 * 4. Jennica - SMS Sent (Awaiting Reply)
 *
 * BEFORE RUNNING:
 * 1. Install dependencies: npm install node-fetch
 * 2. Replace YOUR_API_KEY with your Monday.com API key
 *    (Get it from: monday.com → Profile → Developers → My Access Tokens)
 *
 * TO RUN:
 * node create-jennica-views.js
 */

const BOARD_ID = 18390370563;
const API_KEY = 'YOUR_API_KEY'; // <-- Replace this!

async function createView(name, mutation) {
  console.log(`\n📋 Creating view: ${name}...`);

  try {
    const response = await fetch('https://api.monday.com/v2', {
      method: 'POST',
      headers: {
        'Authorization': API_KEY,
        'Content-Type': 'application/json',
        'API-Version': '2025-04'
      },
      body: JSON.stringify({ query: mutation })
    });

    const result = await response.json();

    if (result.errors) {
      console.log(`   ❌ Error: ${JSON.stringify(result.errors)}`);
      return false;
    }

    if (result.data) {
      const viewData = result.data.create_view_table || result.data.create_view;
      if (viewData) {
        console.log(`   ✅ Created! View ID: ${viewData.id}`);
        return true;
      }
    }

    console.log(`   ⚠️ Unexpected response: ${JSON.stringify(result)}`);
    return false;
  } catch (error) {
    console.log(`   ❌ Error: ${error.message}`);
    return false;
  }
}

async function createAllViews() {
  console.log('='.repeat(60));
  console.log('🟣 CREATING JENNICA\'S VIEWS');
  console.log('='.repeat(60));
  console.log(`Board ID: ${BOARD_ID}`);

  if (API_KEY === 'YOUR_API_KEY') {
    console.log('\n❌ ERROR: Please replace YOUR_API_KEY with your actual Monday.com API key!');
    console.log('   Get it from: monday.com → Profile → Developers → My Access Tokens');
    process.exit(1);
  }

  const views = [
    {
      name: "🟣 Jennica's Day",
      mutation: `
        mutation {
          create_view_table(
            board_id: ${BOARD_ID}
            name: "🟣 Jennica's Day"
            filter: {
              operator: and
              rules: [
                { column_id: "status", compare_value: [5, 4], operator: any_of }
              ]
            }
          ) {
            id
            name
          }
        }
      `
    },
    {
      name: "Jennica - Today's Hunt ⭐",
      mutation: `
        mutation {
          create_view_table(
            board_id: ${BOARD_ID}
            name: "Jennica - Today's Hunt ⭐"
            filter: {
              operator: and
              rules: [
                { column_id: "status", compare_value: [5], operator: any_of }
              ]
            }
          ) {
            id
            name
          }
        }
      `
    },
    {
      name: "Jennica - Timeout Returning Soon",
      mutation: `
        mutation {
          create_view_table(
            board_id: ${BOARD_ID}
            name: "Jennica - Timeout Returning Soon"
            filter: {
              operator: and
              rules: [
                { column_id: "status", compare_value: [4], operator: any_of }
              ]
            }
          ) {
            id
            name
          }
        }
      `
    },
    {
      name: "Jennica - SMS Sent (Awaiting Reply)",
      mutation: `
        mutation {
          create_view_table(
            board_id: ${BOARD_ID}
            name: "Jennica - SMS Sent (Awaiting Reply)"
            filter: {
              operator: and
              rules: [
                { column_id: "status", compare_value: [2], operator: any_of }
              ]
            }
          ) {
            id
            name
          }
        }
      `
    }
  ];

  let successCount = 0;
  let failCount = 0;

  for (const view of views) {
    const success = await createView(view.name, view.mutation);
    if (success) {
      successCount++;
    } else {
      failCount++;
    }
    // Small delay between API calls to avoid rate limiting
    await new Promise(resolve => setTimeout(resolve, 500));
  }

  console.log('\n' + '='.repeat(60));
  console.log('📊 SUMMARY');
  console.log('='.repeat(60));
  console.log(`✅ Successfully created: ${successCount} views`);
  if (failCount > 0) {
    console.log(`❌ Failed: ${failCount} views`);
  }
  console.log('\n💡 Next steps:');
  console.log('   1. Go to Monday.com → Superlative Leads board');
  console.log('   2. Click the view dropdown to see your new views');
  console.log('   3. Configure sorts and column visibility manually in each view');
  console.log('   4. Pin Jennica\'s Day to favorites for quick access');
}

// Run the script
createAllViews().catch(console.error);
