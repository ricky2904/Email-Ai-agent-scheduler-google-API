import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Button,
  Box,
  Alert,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Divider,
  Card,
  CardContent,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import {
  Email,
  Schedule,
  CheckCircle,
  Error,
  Visibility,
  Add
} from '@mui/icons-material';
import axios from 'axios';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

function App() {
  // State for emails
  const [fetchedEmails, setFetchedEmails] = useState([]);
  const [schedulingEmails, setSchedulingEmails] = useState([]);
  
  // State for UI
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [selectedEmail, setSelectedEmail] = useState(null);
  const [emailDialogOpen, setEmailDialogOpen] = useState(false);
  const [schedulingEvent, setSchedulingEvent] = useState(false);

  // Check API health on component mount
  useEffect(() => {
    checkHealth();
  }, []);

  const checkHealth = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      if (!response.data.gmail_connected) {
        setError('Gmail service not connected. Please check your credentials.');
      }
    } catch (err) {
      setError('Backend API not available. Please ensure the backend is running.');
    }
  };

  const fetchEmails = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);
    
    try {
      const response = await axios.get(`${API_BASE_URL}/fetch-emails`);
      setFetchedEmails(response.data.emails);
      setSuccess(`Successfully fetched ${response.data.count} unread emails`);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch emails');
    } finally {
      setLoading(false);
    }
  };

  const fetchSchedulingEmails = async () => {
    setLoading(true);
    setError(null);
    setSuccess(null);
    
    try {
      const response = await axios.get(`${API_BASE_URL}/scheduling-emails`);
      setSchedulingEmails(response.data.scheduling_emails);
      setSuccess(`Found ${response.data.scheduling_count} emails with scheduling information out of ${response.data.total_checked} checked`);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch scheduling emails');
    } finally {
      setLoading(false);
    }
  };

  const scheduleEvent = async (schedulingData) => {
    setSchedulingEvent(true);
    setError(null);
    
    try {
      const response = await axios.post(`${API_BASE_URL}/schedule-event`, {
        scheduling_data: schedulingData
      });
      
      if (response.data.success) {
        setSuccess('Event created successfully in Google Calendar!');
        // Refresh scheduling emails to update the list
        fetchSchedulingEmails();
      } else {
        setError(response.data.message);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to schedule event');
    } finally {
      setSchedulingEvent(false);
    }
  };

  const viewEmailDetails = (email) => {
    setSelectedEmail(email);
    setEmailDialogOpen(true);
  };

  const getStatusColor = (hasScheduling) => {
    return hasScheduling ? 'success' : 'default';
  };

  const getStatusIcon = (hasScheduling) => {
    return hasScheduling ? <CheckCircle /> : <Email />;
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Paper elevation={3} sx={{ p: 3, mb: 3, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
        <Box display="flex" alignItems="center" justifyContent="center">
          <Box textAlign="center">
            <Typography variant="h4" component="h1" color="white" gutterBottom>
              🤖 AI Email Scheduler
            </Typography>
            <Typography variant="subtitle1" color="white" sx={{ opacity: 0.9 }}>
              Automatically extract and schedule events from your emails
            </Typography>
          </Box>
        </Box>
      </Paper>

      {/* Status Messages */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      {success && (
        <Alert severity="success" sx={{ mb: 2 }} onClose={() => setSuccess(null)}>
          {success}
        </Alert>
      )}

      {/* Action Buttons */}
      <Box display="flex" justifyContent="center" gap={2} sx={{ mb: 4 }}>
        <Button
          variant="contained"
          size="large"
          startIcon={<Email />}
          onClick={fetchEmails}
          disabled={loading}
          sx={{ 
            minWidth: 200, 
            height: 60,
            fontSize: '1.1rem',
            fontWeight: 'bold'
          }}
        >
          {loading ? <CircularProgress size={24} /> : 'Fetch Emails'}
        </Button>
        
        <Button
          variant="contained"
          color="secondary"
          size="large"
          startIcon={<Schedule />}
          onClick={fetchSchedulingEmails}
          disabled={loading}
          sx={{ 
            minWidth: 250, 
            height: 60,
            fontSize: '1.1rem',
            fontWeight: 'bold'
          }}
        >
          {loading ? <CircularProgress size={24} /> : 'Scheduled Meeting Emails'}
        </Button>
      </Box>

      {/* Fetched Emails Section */}
      {fetchedEmails.length > 0 && (
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
            <Email /> All Unread Emails ({fetchedEmails.length})
          </Typography>
          
          <List>
            {fetchedEmails.map((email, index) => (
              <React.Fragment key={email.id || index}>
                <ListItem
                  sx={{
                    '&:hover': { backgroundColor: 'action.hover' },
                    borderRadius: 1,
                    mb: 1
                  }}
                >
                  <ListItemText
                    primary={
                      <Typography variant="subtitle1" fontWeight="medium">
                        {email.subject || 'No Subject'}
                      </Typography>
                    }
                    secondary={
                      <Box>
                        <Typography variant="body2" color="textSecondary" gutterBottom>
                          From: {email.from || 'Unknown'}
                        </Typography>
                        <Typography variant="body2" noWrap>
                          {email.snippet || 'No preview available'}
                        </Typography>
                      </Box>
                    }
                  />
                  <ListItemSecondaryAction>
                    <IconButton
                      edge="end"
                      onClick={() => viewEmailDetails(email)}
                      color="primary"
                    >
                      <Visibility />
                    </IconButton>
                  </ListItemSecondaryAction>
                </ListItem>
                {index < fetchedEmails.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </Paper>
      )}

      {/* Scheduling Emails Section */}
      {schedulingEmails.length > 0 && (
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
          <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
            <Schedule /> Emails with Scheduling Information ({schedulingEmails.length})
          </Typography>
          
          <List>
            {schedulingEmails.map((email, index) => (
              <React.Fragment key={email.email_id || index}>
                <ListItem
                  sx={{
                    '&:hover': { backgroundColor: 'action.hover' },
                    borderRadius: 1,
                    mb: 1
                  }}
                >
                  <ListItemText
                    primary={
                      <Box display="flex" alignItems="center" gap={1} mb={1}>
                        <Typography variant="subtitle1" fontWeight="medium">
                          {email.subject || 'No Subject'}
                        </Typography>
                        <Chip
                          icon={getStatusIcon(email.has_scheduling)}
                          label="Has Scheduling"
                          color={getStatusColor(email.has_scheduling)}
                          size="small"
                        />
                      </Box>
                    }
                    secondary={
                      <Box>
                        <Typography variant="body2" color="textSecondary" gutterBottom>
                          From: {email.from || 'Unknown'}
                        </Typography>
                        <Typography variant="body2" noWrap>
                          {email.snippet || 'No preview available'}
                        </Typography>
                        {email.scheduling_data && (
                          <Box mt={1}>
                            <Typography variant="body2" color="primary" fontWeight="medium">
                              Event: {email.scheduling_data.title} on {email.scheduling_data.date} at {email.scheduling_data.start_time}
                            </Typography>
                          </Box>
                        )}
                      </Box>
                    }
                  />
                  <ListItemSecondaryAction>
                    <Box display="flex" gap={1}>
                      <IconButton
                        edge="end"
                        onClick={() => viewEmailDetails(email)}
                        color="primary"
                      >
                        <Visibility />
                      </IconButton>
                      {email.scheduling_data && (
                        <Button
                          variant="contained"
                          size="small"
                          startIcon={<Add />}
                          onClick={() => scheduleEvent(email.scheduling_data)}
                          disabled={schedulingEvent}
                          color="success"
                        >
                          {schedulingEvent ? <CircularProgress size={16} /> : 'Schedule'}
                        </Button>
                      )}
                    </Box>
                  </ListItemSecondaryAction>
                </ListItem>
                {index < schedulingEmails.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        </Paper>
      )}

      {/* Empty State */}
      {fetchedEmails.length === 0 && schedulingEmails.length === 0 && !loading && (
        <Box textAlign="center" py={8}>
          <Email sx={{ fontSize: 64, color: 'grey.300', mb: 2 }} />
          <Typography variant="h6" color="textSecondary">
            No emails loaded yet
          </Typography>
          <Typography variant="body2" color="textSecondary">
            Click one of the buttons above to fetch emails
          </Typography>
        </Box>
      )}

      {/* Email Details Dialog */}
      <Dialog 
        open={emailDialogOpen} 
        onClose={() => setEmailDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Email Details
        </DialogTitle>
        <DialogContent>
          {selectedEmail && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Subject: {selectedEmail.subject || selectedEmail.subject}
              </Typography>
              <Typography variant="body2" color="textSecondary" gutterBottom>
                From: {selectedEmail.from || selectedEmail.from}
              </Typography>
              <Divider sx={{ my: 2 }} />
              <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                {selectedEmail.snippet || selectedEmail.snippet}
              </Typography>
              {selectedEmail.scheduling_data && (
                <Box mt={2}>
                  <Typography variant="h6" gutterBottom>
                    Scheduling Information:
                  </Typography>
                  <Card sx={{ p: 2, bgcolor: 'grey.50' }}>
                    <Typography variant="body2">
                      <strong>Title:</strong> {selectedEmail.scheduling_data.title}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Date:</strong> {selectedEmail.scheduling_data.date}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Time:</strong> {selectedEmail.scheduling_data.start_time} - {selectedEmail.scheduling_data.end_time}
                    </Typography>
                    {selectedEmail.scheduling_data.location && (
                      <Typography variant="body2">
                        <strong>Location:</strong> {selectedEmail.scheduling_data.location}
                      </Typography>
                    )}
                    {selectedEmail.scheduling_data.participants && selectedEmail.scheduling_data.participants.length > 0 && (
                      <Typography variant="body2">
                        <strong>Participants:</strong> {selectedEmail.scheduling_data.participants.join(', ')}
                      </Typography>
                    )}
                  </Card>
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEmailDialogOpen(false)}>
            Close
          </Button>
          {selectedEmail && selectedEmail.scheduling_data && (
            <Button
              onClick={() => {
                scheduleEvent(selectedEmail.scheduling_data);
                setEmailDialogOpen(false);
              }}
              variant="contained"
              disabled={schedulingEvent}
              startIcon={schedulingEvent ? <CircularProgress size={20} /> : <Add />}
            >
              {schedulingEvent ? 'Scheduling...' : 'Schedule Event'}
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Container>
  );
}

export default App;