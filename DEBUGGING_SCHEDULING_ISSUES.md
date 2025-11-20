# 🔍 Debugging Scheduled Email Detection Issues

## ✅ Changes Made

### 1. **Enhanced Detection Logic** (`app.py`)
- Now checks **both** conditions:
  - No "action" key present
  - Valid date AND start_time exist
- Added detailed logging for each email analysis

### 2. **Improved LLM Response Handling** (`llm_agent.py`)
- Returns proper "no scheduling" format if date/time missing
- Better null/empty value handling
- Added debug print statements

### 3. **New Debug Endpoint**
- `/api/debug-scheduling` - Test scheduling detection with custom text

## 🐛 How to Debug

### Step 1: Check Backend Logs

When you click "Fetch Emails", check the backend terminal for:
```
📧 Analyzing email: [Subject]
📊 Parsed data keys: [...]
📊 Has 'action' key: True/False
📊 Has date: True/False (actual value)
📊 Has start_time: True/False (actual value)
📊 Has valid scheduling: True/False
```

### Step 2: Use Debug Endpoint

Test with a sample email:
```bash
curl "http://localhost:5000/api/debug-scheduling?text=Meeting%20tomorrow%20at%203pm%20in%20room%20A"
```

This will show you:
- What the LLM returns
- How it's parsed
- Whether it would be detected
- Why it's detected or not

### Step 3: Check LLM Output

Look for these in backend logs:
```
🔍 Raw LLM Output: [LLM response]
✅ Valid scheduling data found: date=..., start_time=...
```

OR

```
⚠️ Missing required fields: date=True/False, start_time=True/False
```

## 🔧 Common Issues & Fixes

### Issue 1: LLM Returns Null Values
**Symptom**: Date or start_time are `null` in JSON
**Fix**: The code now handles this and marks as "no scheduling"

### Issue 2: LLM Doesn't Extract Date/Time Properly
**Symptom**: LLM returns data but date/time are empty strings
**Fix**: Check the prompt in `llm_agent.py` - ensure it's clear about date/time format

### Issue 3: Detection Logic Not Working
**Symptom**: Emails with scheduling aren't detected
**Fix**: Check logs to see which condition fails:
- `has_action_key` should be False
- `has_valid_scheduling` should be True

### Issue 4: Cache Not Populating
**Symptom**: Clicking "Scheduled Meeting Emails" shows empty
**Fix**: 
1. Make sure you clicked "Fetch Emails" first
2. Check backend logs for "✅ Email ... has scheduling content!"
3. Verify cache_count in debug endpoint

## 📊 Detection Criteria

An email is considered to have scheduling content if:
1. ✅ **No "action" key** in parsed data (LLM didn't say "no scheduling")
2. ✅ **Has valid date** - non-empty string after stripping
3. ✅ **Has valid start_time** - non-empty string after stripping

Both conditions must be true!

## 🧪 Testing

### Test 1: Basic Detection
```bash
# Should detect scheduling
curl "http://localhost:5000/api/debug-scheduling?text=Meeting%20on%202025-11-05%20at%203:00pm"
```

### Test 2: No Scheduling
```bash
# Should NOT detect scheduling
curl "http://localhost:5000/api/debug-scheduling?text=Just%20a%20regular%20email"
```

### Test 3: Real Email
```bash
# Test with actual email snippet from Gmail
curl "http://localhost:5000/api/debug-scheduling?text=[paste%20email%20snippet%20here]"
```

## 📝 Next Steps

1. **Restart backend** to get new debug logging
2. **Click "Fetch Emails"** and watch backend logs
3. **Check debug endpoint** if issues persist
4. **Share backend logs** if still not working

The enhanced logging will show exactly why emails are or aren't being detected!




