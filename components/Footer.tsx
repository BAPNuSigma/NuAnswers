import React from 'react';
import { Box, Container, Typography, Link, Grid } from '@mui/material';

const Footer = () => {
  return (
    <Box component="footer" sx={{ bgcolor: 'background.paper', py: 6, mt: 'auto' }}>
      <Container maxWidth="lg">
        <Grid container spacing={4} justifyContent="space-between">
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              About NuAnswers
            </Typography>
            <Typography variant="body2" color="text.secondary">
              An AI-powered tutoring platform designed to help Northwestern students excel in their studies.
            </Typography>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Legal
            </Typography>
            <Link href="/legal/privacy-policy" color="text.secondary" display="block">
              Privacy Policy
            </Link>
            <Link href="/legal/terms-of-service" color="text.secondary" display="block">
              Terms of Service
            </Link>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Contact
            </Typography>
            <Link href="/contact" color="text.secondary" display="block">
              Contact Us
            </Link>
            <Typography variant="body2" color="text.secondary">
              support@nuanswers.org
            </Typography>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Security
            </Typography>
            <Typography variant="body2" color="text.secondary">
              SSL Secured
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Data Protection Compliant
            </Typography>
          </Grid>
        </Grid>
        
        <Box mt={5}>
          <Typography variant="body2" color="text.secondary" align="center">
            {'© '}
            {new Date().getFullYear()}
            {' NuAnswers. All rights reserved.'}
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer; 